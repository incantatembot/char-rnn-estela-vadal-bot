
# coding: utf-8

import sys
import os
import re
import json
import time
import subprocess
from random import randint

# for generating seed text
import random
import string

config = {}
config['SCRIPT_PATH'] = '/home/estelavadal'
config['CHARRNN_PATH'] = '/home/estelavadal/char-rnn'
config['RNN_MODEL_PATH'] = '/home/estelavadal/models/estela.v.808.t7'
config['MAX_LINE_LENGTH'] = 500
config['NUM_SKIP_LINES'] = 1

config['VALID_WORDS'] = []

config['VALID_WORDS'] = set(line.strip() for line in open('dictionary.txt'))

#print "VALID WORDS:"
#print config['VALID_WORDS']

def is_sentence_valid(sentence):
    sentence_temp = str(sentence)
    # strip all punctuations, convert to lowercase
    sentence_temp = sentence_temp.translate(None, string.punctuation)
    sentence_temp = sentence_temp.lower()
    word_list = sentence_temp.split()

    # compare against our dictionary
    for word in word_list:
        if word not in config['VALID_WORDS']: 
            print "Invalid word found: [" + str(word) + "] in: [" + str(sentence) + "]"
            return False

    return True



def generate_poetry():
    unique_chars_list = ['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'J', 'M', 'L', 'O', 'N', 'Q', 'P', 'S', 'R', 'U', 'T', 'W', 'V', 'Y', 'Z', 'a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 's', 'r', 'u', 't', 'w', 'v', 'y', 'z']
    seedTextA = ''.join([random.choice(unique_chars_list) for n in xrange(randint(2, 7))])
    seedTextB = ''.join([random.choice(unique_chars_list) for n in xrange(randint(2, 7))])
    seedTextC = ''.join([random.choice(unique_chars_list) for n in xrange(randint(2, 7))])
    seedText = seedTextA + ' ' + seedTextB + ' ' + seedTextC
    
    # generate temperature from 0.4000 to 0.6999
    tempA = float(randint(4, 6))
    tempB = float(randint(0, 9))
    tempC = float(randint(0, 9))
    tempD = float(randint(0, 9))
    temperature = float(0.0 + tempA/10 + tempB/100 + tempC/1000 + tempD/10000)

    # print "Seed Text:\t", seedText
    # print "Temperature:\t", str(temperature)

    os.chdir(config['CHARRNN_PATH'])

    rnn_cmd_list = [
        'th',
        'sample.lua',
        config['RNN_MODEL_PATH'],
        '-length',
        '1024',
        '-verbose',
        '0',
        '-temperature',
        str(temperature),
        '-primetext',
        seedText.encode('utf8'),
        '-gpuid',
        '-1'
    ]

    rnn_proc = subprocess.Popen(
        rnn_cmd_list,
        stdout=subprocess.PIPE
    )
    raw_poetry = rnn_proc.stdout.read().decode('utf8')

    # print "RAW OUTPUT:"
    # print repr(raw_poetry)
    
    raw_poetry_per_line = filter(lambda y: y, map(lambda x: x.strip(), raw_poetry.split(u'\n')))
    
    # print "LINES:"
    # print repr(raw_poetry_per_line)
    
    chars_remaining = config['MAX_LINE_LENGTH']

    # let's build our tweet
    poetic_lines = []
    for i, line in enumerate(raw_poetry_per_line):
        # skip processing the last line
        if len(raw_poetry_per_line) == i+1:
            break
            
        # if we still have space, append
        if i >= config['NUM_SKIP_LINES'] and config['MAX_LINE_LENGTH'] >= len(line):
            if is_sentence_valid(line):
                poetic_lines.append(u''+line)

    # print "TWEETS:"
    # print repr(poetic_lines)

    # Back to original working directory
    os.chdir(config['SCRIPT_PATH'])
    
    return poetic_lines

state = {}
state['lines_of_poetry'] = []
state['lines_of_poetry_counter'] = 0

def get_poetic_line():
    # reset queue if we've used every queued item
    if(state['lines_of_poetry_counter'] >= len(state['lines_of_poetry'])):
        state['lines_of_poetry'] = []
        state['lines_of_poetry_counter'] = 0

    while (len(state['lines_of_poetry']) == 0):
        # print "GENERATING POETRY..."
        state['lines_of_poetry'] = generate_poetry()
        state['lines_of_poetry_counter'] = 0

    current_index = state['lines_of_poetry_counter']
    current_poetic_line = state['lines_of_poetry'][current_index]
    state['lines_of_poetry_counter'] += 1
    return current_poetic_line

while 1:
    line = get_poetic_line()
    print line
    time.sleep(1)