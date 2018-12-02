from os import environ

import requests
from celery import Celery
from celery.utils.log import get_task_logger

# Celery logger, rather than logging.getLogger, for task ids in logs
log = get_task_logger(__name__)

# TODO: Use shared tasks?
# Declare the celery app object
app = Celery('celery', broker=environ['SBF_CELERY_BROKER'])
# 5 minute time limit on tasks - even this is kind of preposterous
app.conf.task_time_limit = 60*5
# 3 minute soft time limit, if a task needs to catch that exception
app.conf.task_soft_time_limit = 60*3


def parse_api_response(resp):
    """
    Parses the response from calling the Slack API
    Logs if anything went wrong

    :param response resp: A `requests.Response` object
    :rtype: None
    """
    # If this goes off something went really wrong - the Slack API should respond with 200's
    # Even if there an error (which is in the JSON)
    resp.raise_for_status()
    try:
        reply_json = resp.json()
    # TODO:Handle
    except Exception as e:
        raise e
    if not reply_json['ok']:
        # Something went wront - Slack gave us back an error
        log.error(str(reply_json))


def say_something(channel, msg):
    """
    Respond in a specific channel as the bot

    :param str channel: The channel identifier
    :param str msg: The message to the send to the channel

    :rtype None:
    """
    try:
        # Slack is picky about including the encoding on the Content-Type header
        resp = requests.post(
            "https://slack.com/api/chat.postMessage?charset=utf8",
            json={
                "token": environ['SBF_BOT_OAUTH_TOKEN'],
                "channel": channel,
                "text": "Hello World!"
            },
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': 'Bearer {}'.format(
                    environ['SBF_BOT_OAUTH_TOKEN']
                )
            },
            timeout=10
        )
        parse_api_response(resp)
    except requests.exceptions.Timeout as e:
        log.exception(e)


@app.task
def hello_world(slack_event_json):
    """
    Say hello world

    :param dict slack_event_json: The json from the Slack events API

    :rtype: None
    """
    channel = slack_event_json['event']['channel']
    # Post the reply
    say_something(channel, "Hello World!")
