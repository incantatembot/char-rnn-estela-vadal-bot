# coding: utf-8
import sys
import os
import shutil
import re
import json
import time
import subprocess
import datetime
import hashlib
import urllib
import logging
from random import randint

# for generating seed text
import random
import string

import warnings
import os
from flask import Flask, request

import requests

import sched
import time
from threading import Timer

SPACE_LENGTH = 1
RESPONSE_LIMIT = 300

class Queue:
    def __init__(self):
        self.items = set()

    def isEmpty(self):
        return self.size() == 0

    def enqueue(self, item):
        self.items.add(item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

message_queue = Queue()
message_queue_contents = {}

app = Flask(__name__)

FACEBOOK_TOKEN = "YOUR FACEBOOK TOKEN"
VERIFY_TOKEN = "YOUR VERIFICATION TOKEN"

class EstelaVadal(object):
    def __init__(self):
        self.screen_name = "estelavadal"
        self.model_path = "/home/estelavadal/models/estela.v.810.t7"
        self.char_rnn_path = "/home/estelavadal/char-rnn"
        self.script_path = "/home/facebook-chatbot"

        self.unique_chars_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', ' ', '.', '?', '!', ':']

        self.dictionary_path = "/home/estelavadal/old-files/dictionary.txt.orig"
        self.valid_words = set(line.strip() for line in open(self.dictionary_path))

        self.logging_level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=self.screen_name + '.log',
            level=self.logging_level)

        self.line_counter = 0
        self.line_database = []
        self.seed_text = ""

    def log(self, message, level=logging.INFO):
        if level == logging.ERROR:
            logging.error(message)
        else:
            logging.info(message)

    def clean_seed_text(self, seed_text):
        cleaned_seed_text = ""
        for c in str(seed_text):
            if c in self.unique_chars_list:
                cleaned_seed_text = cleaned_seed_text + str(c)
            else:
                cleaned_seed_text = cleaned_seed_text + str(" ")
        return cleaned_seed_text

    def is_sentence_valid(self, sentence):
        # if we don't have a dictionary, then everything is valid
        if not self.valid_words:
            return True

        sentence_temp = str(sentence)
        sentence_temp = sentence_temp.translate(None, string.punctuation)
        sentence_temp = sentence_temp.lower()
        word_list = sentence_temp.split()

        # compare against our dictionary
        for word in word_list:
            if word not in self.valid_words:
                return False

        return True

    def generate_text(self):
        # generate temperature from 0.4000 to 0.6999
        tempA = float(randint(4, 6))
        tempB = float(randint(0, 9))
        tempC = float(randint(0, 9))
        tempD = float(randint(0, 9))
        temperature = float(0.0 + tempA/10 + tempB/100 + tempC/1000 + tempD/10000)

        self.char_per_line = 100 # average character per line
        text_length = 10000

        seed_text = ""
        if len(self.seed_text) == 0:
            sha_1 = hashlib.sha1()
            current_date_time = str(datetime.datetime.now())
            sha_1.update(current_date_time)
            seed_text = str(sha_1.hexdigest())
        else:
            seed_text = self.seed_text
            self.seed_text = ""

        seed_text = self.clean_seed_text(seed_text).strip()

        self.log("######################")
        self.log("Seed Text: " + str(seed_text))
        self.log("Temperature: " + str(temperature))

        os.chdir(self.char_rnn_path)

        rnn_cmd_list = [
            'th',
            'sample.lua',
            self.model_path,
            '-length',
            str(text_length),
            '-verbose',
            '0',
            '-temperature',
            str(temperature),
            '-primetext',
            seed_text.encode('utf8'),
            '-gpuid',
            '-1'
        ]

        rnn_proc = subprocess.Popen(
            rnn_cmd_list,
            stdout=subprocess.PIPE
        )
        raw_text = rnn_proc.stdout.read().decode('utf8')

        raw_text_per_line = filter(lambda y: y, map(lambda x: x.strip(), raw_text.split(u'\n')))

        output_lines_length = len(raw_text_per_line)
        response_lines = []
        for i, line in enumerate(raw_text_per_line):
            # skip processing the last line
            if output_lines_length == i+1:
                break

            # skip first line
            if i >= 1:
                if self.is_sentence_valid(line):
                    response_lines.append(line)

        os.chdir(self.script_path)
        self.log("Generated text:")
        self.log(response_lines)
        self.log("######################")
        return response_lines

    def get_response(self, message):
        num_lines = randint(1, 5)
        response = ""
        for x in range(0, num_lines):
            if not self.line_database or self.line_counter >= len(self.line_database):
                del self.line_database[:]
                # if we don't have a seed text, use the message as seed text
                if len(self.seed_text) == 0:
                    self.seed_text = message.strip()

                self.line_database = self.generate_text()
                self.line_counter = 0

            if len(response + " " + self.line_database[self.line_counter]) > RESPONSE_LIMIT:
                break
            else:
                if x == 0:
                    response = self.line_database[self.line_counter]
                else:
                    response = response + " " + self.line_database[self.line_counter]

                # use latest line as next seed text
                self.seed_text = self.line_database[self.line_counter]

                self.line_counter = self.line_counter + 1

        return response

estelavadal = EstelaVadal()

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    estelavadal.log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data.get("object") and data["object"] == "page":
        if data.get("entry") and data["entry"]:
            for entry in data["entry"]:
                if entry.get("messaging") and entry["messaging"]:
                    for messaging_event in entry["messaging"]:

                        if messaging_event.get("message"):  # someone sent us a message
                            if messaging_event["message"].get("text"):
                                sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                                recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                                message_text = messaging_event["message"]["text"]  # the message's text

                                message_queue.enqueue(str(sender_id))

                                try:
                                    message_text = ''.join([i if ord(i) < 128 else ' ' for i in message_text])
                                    message_queue_contents[sender_id] = str(message_text)
                                except:
                                    message_queue_contents[sender_id] = ""
                                    message_text = ""

                                estelavadal.log("Message queued: sender_id %s, message_text %s" % (str(sender_id), str(message_text)))

                        if messaging_event.get("delivery"):  # delivery confirmation
                            pass

                        if messaging_event.get("optin"):  # optin confirmation
                            pass

                        if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                            pass

    return "OK", 200


def send_message(recipient_id, message_text):

    estelavadal.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": FACEBOOK_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        estelavadal.log(r.status_code)
        estelavadal.log(r.text)

def check_message_queue():
    if 0 < message_queue.size():
        sender_id = message_queue.dequeue()
        message_text = message_queue_contents[sender_id]
        if (0 < len(message_text)):
            estelavadal.log("Processing response for: sender_id %s, message_text %s" % (str(sender_id), str(message_text)))

            response_text = estelavadal.get_response(message_text)
            estelavadal.log("response_text: %s" % str(response_text))

            send_message(sender_id, response_text)
            message_queue_contents[sender_id] = ""
    else:
        message_queue_contents.clear()

    Timer(10, check_message_queue, ()).start()

Timer(10, check_message_queue, ()).start()

if __name__ == '__main__':
    app.run(port=924, debug=True)
