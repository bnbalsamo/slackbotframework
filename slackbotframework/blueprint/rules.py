from .celery import hello_world


def require_channel(slack_event_json):
    """
    Require a channel be present in the JSON from the Events API

    :params dict slack_event_json: The JSON from the events API

    :rtype: bool (False) or str
    """
    # Get the channel, else false so we
    # don't reply to mention without channel info
    # eg: mentions in channels the bot isn't in
    event = slack_event_json.get('event')
    if event is None:
        return False
    channel = event.get('channel')
    if not channel:
        return False
    return channel


def hello_world_rule(slack_event_json):
    """
    If a channel is present, True, else False
    """
    if require_channel(slack_event_json) is None:
        return False
    return True


#: A list of tuples, where the first element is a conditional function
#: that should accept the JSON from the slack event API as the only arg,
#: and the second element is a celery task function which should accept
#: the JSON from te slack event API as the only arg.
rule_list = [
    (hello_world_rule, hello_world)
]
