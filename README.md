# char-rnn-estela-vadal-bot
A Multi-layer Recurrent Neural Networks (LSTM) Twitter bot that generates character-level poetry in Filipino.

Follow her at https://twitter.com/estelavadal.

## Requirements
1. Install [char-rnn](https://github.com/karpathy/char-rnn#requirements) pre-requisites.
2. Install [twitterbot](https://github.com/thricedotted/twitterbot).
3. Clone the repository files to /home/estelavadal. If you want to clone the repository somewhere else, you'll need to edit the following files:
    * ano-ang-mga-lihim-ng-mundo.py
        * `config['SCRIPT_PATH']`
        * `config['CHARRNN_PATH']`
        * `config['RNN_MODEL_PATH']`
    * estelavadal.py
        * `self.config['SCRIPT_PATH']`
        * `self.config['CHARRNN_PATH']`
        * `self.config['RNN_MODEL_PATH']`
4. If you want to run your own Twitter bot, you'll need to plug-in your own access keys (check this [guide](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/) for more details) to estelavadal.py:
    * self.config['api_key'] = ''<YOUR TWITTER API KEY>''
    * self.config['api_secret'] = ''<YOUR TWITTER API SECRET>''
    * self.config['access_key'] = '<YOUR TWITTER ACCESS KEY>'
    * self.config['access_secret'] = '<YOUR TWITTER ACCESS SECRET>'

## Usage
To generate text:

    $ python ano-ang-mga-lihim-ng-mundo.py
    
To run the twitter bot:

    $ python estelavadal.py

## Software License Information

MIT License

Copyright (c) 2017 matangkuwago

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

