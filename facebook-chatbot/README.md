# facebook-chatbot-python
A simple python chatbot for Facebook Messenger forked from [facebook-chatbot-python](https://github.com/hult/facebook-chatbot-python).

The bot reads incoming Facebook Messenger messages, and responds by picking lines from generated random text via its neural network engine.

## Installing dependencies

Use of virtualenv is highly recommended.

    $ pip install -r requirements.txt

## Setting up a Facebook app for Facebook messenger

* You're going to need a publicly routed https address. I used [ngrok](https://ngrok.com/) to create a tunnel to my local development machine.
* The server will need to be started for you to verify the webhook. See "Starting the server" below.
* Follow the instructions provided in the [Facebook quickstart tutorial](https://developers.facebook.com/docs/messenger-platform/quickstart) for creating a page and an app.
* Set the `VERIFY_TOKEN` and `FACEBOOK_TOKEN` environment variables to the values you get from following the tutorial.

## Starting the server

Is just a matter of

    $ python server.py
