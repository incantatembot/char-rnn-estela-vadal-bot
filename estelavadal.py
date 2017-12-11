#!/usr/bin/env python2
# -*- coding: utf-8 -*- #
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

from twitterbot import TwitterBot

class EstelaVadal(TwitterBot):
    def bot_init(self):
        """
        Initialize and configure your bot!

        Use this function to set options and initialize your own custom bot
        state (if any).
        """

        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################
        self.config['api_key'] = '<YOUR TWITTER API KEY>'
        self.config['api_secret'] = '<YOUR TWITTER API SECRET>'
        self.config['access_key'] = '<YOUR TWITTER ACCESS KEY>'
        self.config['access_secret'] = '<YOUR TWITTER ACCESS SECRET>'


        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = 1 * 60 * 60     # every hour

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = None

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

        # path where this script is located
        self.config['SCRIPT_PATH'] = '/home/estelavadal'

        # char-rnn's path; sampling will be done on this directory
        self.config['CHARRNN_PATH'] = '/home/estelavadal/char-rnn'

        # char-rnn model location
        self.config['RNN_MODEL_PATH'] = '/home/estelavadal/models/estela.v.810.t7'

        # maximum tweet length
        self.config['MAX_TWEET_LENGTH'] = 200

        # skip the first line since that will contain rubbish (seed text)
        self.config['NUM_SKIP_LINES'] = 1

        # load dictionary of valid words
        self.config['VALID_WORDS'] = set(line.strip() for line in open('dictionary.txt'))

        ###########################################
        # CUSTOM: your bot's own state variables! #
        ###########################################
        
        # If you'd like to save variables with the bot's state, use the
        # self.state dictionary. These will only be initialized if the bot is
        # not loading a previous saved state.
        self.state['lines_of_poetry'] = []
        self.state['lines_of_poetry_counter'] = 0

        # You can also add custom functions that run at regular intervals
        # using self.register_custom_handler(function, interval).
        #
        # For instance, if your normal timeline tweet interval is every 30
        # minutes, but you'd also like to post something different every 24
        # hours, you would implement self.my_function and add the following
        # line here:
        
        # self.register_custom_handler(self.my_function, 60 * 60 * 24)


    def on_scheduled_tweet(self):
        """
        Make a public tweet to the bot's own timeline.

        It's up to you to ensure that it's less than 140 characters.

        Set tweet frequency in seconds with TWEET_INTERVAL in config.py.
        """
        text = self.get_poetic_line()
        self.post_tweet(text)


    def on_mention(self, tweet, prefix):
        """
        Defines actions to take when a mention is received.

        tweet - a tweepy.Status object. You can access the text with
        tweet.text

        prefix - the @-mentions for this reply. No need to include this in the
        reply string; it's provided so you can use it to make sure the value
        you return is within the 140 character limit with this.

        It's up to you to ensure that the prefix and tweet are less than 140
        characters.

        When calling post_tweet, you MUST include reply_to=tweet, or
        Twitter won't count it as a reply.
        """
        
        text = self.get_poetic_line()
        self.post_tweet(prefix + ' ' + text, reply_to=tweet)


    def on_timeline(self, tweet, prefix):
        """
        Defines actions to take on a timeline tweet.

        tweet - a tweepy.Status object. You can access the text with
        tweet.text

        prefix - the @-mentions for this reply. No need to include this in the
        reply string; it's provided so you can use it to make sure the value
        you return is within the 140 character limit with this.

        It's up to you to ensure that the prefix and tweet are less than 140
        characters.

        When calling post_tweet, you MUST include reply_to=tweet, or
        Twitter won't count it as a reply.
        """

        text = self.get_poetic_line()
        self.post_tweet(prefix + ' ' + text, reply_to=tweet)


    def is_sentence_valid(self, sentence):
        sentence_temp = str(sentence)
        # strip all punctuations, convert to lowercase
        sentence_temp = sentence_temp.translate(None, string.punctuation)
        sentence_temp = sentence_temp.lower()
        word_list = sentence_temp.split()

        # compare against our dictionary
        for word in word_list:
            if word not in self.config['VALID_WORDS']: 
                print("Invalid word found: [" + str(word) + "] in: [" + str(sentence) + "]")
                return False

        return True

    def generate_poetry(self):
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

        print "Seed Text:\t", seedText
        print "Temperature:\t", str(temperature)

        os.chdir(self.config['CHARRNN_PATH'])

        rnn_cmd_list = [
            'th',
            'sample.lua',
            self.config['RNN_MODEL_PATH'],
            '-length',
            '2048',
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

        raw_poetry_per_line = filter(lambda y: y, map(lambda x: x.strip(), raw_poetry.split(u'\n')))

        chars_remaining = self.config['MAX_TWEET_LENGTH']

        # let's build our tweet
        poetic_lines = []
        for i, line in enumerate(raw_poetry_per_line):
            # skip processing the last line since it is usually truncated
            if len(raw_poetry_per_line) == i+1:
                break
                
            # check if line is tweetable
            if i >= self.config['NUM_SKIP_LINES'] and self.config['MAX_TWEET_LENGTH'] >= len(line):
                if self.is_sentence_valid(line):
                    poetic_lines.append(u''+line)

        # Back to original working directory
        os.chdir(self.config['SCRIPT_PATH'])
        
        return poetic_lines

    def get_poetic_line(self):
        # reset queue and counter if queue is empty
        if(self.state['lines_of_poetry_counter'] >= len(self.state['lines_of_poetry'])):
            self.state['lines_of_poetry'] = []
            self.state['lines_of_poetry_counter'] = 0

        # generate lines if queue is empty
        while (len(self.state['lines_of_poetry']) == 0):
            self.state['lines_of_poetry'] = self.generate_poetry()
            self.state['lines_of_poetry_counter'] = 0

        # return a line and update the counter
        current_index = self.state['lines_of_poetry_counter']
        current_poetic_line = self.state['lines_of_poetry'][current_index]
        self.state['lines_of_poetry_counter'] += 1
        return current_poetic_line

if __name__ == '__main__':
    bot = EstelaVadal()
    bot.run()
