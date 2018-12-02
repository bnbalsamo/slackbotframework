# Slack Bot Framework [![v0.0.1](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/bnbalsamo/slackbotframework/releases)

[![Build Status](https://travis-ci.org/bnbalsamo/slackbotframework.svg?branch=master)](https://travis-ci.org/bnbalsamo/slackbotframework) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/slackbotframework/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/slackbotframework?branch=master) [![Documentation Status](https://readthedocs.org/projects/slackbotframework/badge/?version=latest)](http://slack-bot-framework.readthedocs.io/en/latest/?badge=latest)

A framework for building internal integration slack bots

The Slack Bot Framework is meant to be a minimalistic framework for writing [internal integrations](https://api.slack.com/internal-integrations).

It uses a flask web application to accept connections from the slack application and events APIs, and maps a series of conditional rules onto celery tasks. JSON payloads delivered to the web frontend which satisfy one of the configured conditionals are then queued for processing via a celery worker task.

The project ships with a hello world implementation, which will cause the bot to reply "Hello World!" to every event it receives. Remove that task, or add more, by editing slackbotframework/blueprint/celery.py to include any required task logic, and editing slackbotframework/blueprint/rules.py to include a tuple in the rules_list with a conditional callback and a reference to the task.

In order to configure the bot, create an application within slack, include a bot user with the "mentions" scope, and then supply the required configuration variables to the application, which should be running at the URL you point the slack application at. After that, once the bot has been invited to the channel, it should start replying with "Hello World!"


See the full documentation at https://slack-bot-framework.readthedocs.io


# Author
Brian Balsamo <Brian@BrianBalsamo.com>
