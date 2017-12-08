# char-rnn-estela-vadal-bot
A Multi-layer Recurrent Neural Networks (LSTM) Twitter bot that generates character-level poetry in Filipino.

Follow her at https://twitter.com/estelavadal. She tweets regularly and she responds to mentions.

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
