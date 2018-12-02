"""
SBF
"""

import logging
import hmac
import hashlib

from flask import Blueprint, Response, request, abort
from flask_restful import Resource, Api

from .rules import rule_list


__author__ = "Brian Balsamo"
__email__ = "Brian@BrianBalsamo.com"
__version__ = "0.0.1"


BLUEPRINT = Blueprint('slackbotframework', __name__)
BLUEPRINT.config = {}

API = Api(BLUEPRINT)

log = logging.getLogger(__name__)


def verify_request():
    """
    Uses Slacks hmac impl. to determine that a request
    originated from Slack itself

    :rtype: bool
    """
    log.debug("Verifying request signature")
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    sig = request.headers.get('X-Slack-Signature')
    if timestamp is None or sig is None:
        abort(403)
    # Lifted from the slack python sdk, slight alterations
    req = str.encode('v0:' + str(timestamp) + ':') + request.data
    request_hash = 'v0=' + hmac.new(
        str.encode(BLUEPRINT.config['SIGNING_SECRET']),
        req, hashlib.sha256
    ).hexdigest()
    if hmac.compare_digest(request_hash, sig):
        log.debug("Received request with correct signature")
        return True
    else:
        log.warn("Received request with bad signature")
        return False


def is_verification_handshake(rjson):
    """
    Determines if the request is the Slack application APIs verification handshake

    :rtype: bool
    """
    # Check body contains the right keys
    for x in ['token', 'challenge', 'type']:
        if x not in rjson:
            return False
    # Check type is correct
    if rjson['type'] != "url_verification":
        return False
    # Note: no need to check the token, we check the request is signed
    # before this code is ever run.

    # It's a verification request
    log.info("Received URL verification handshake request")
    return True


class Root(Resource):
    """
    POST endpoint to catch all the data from the Slack Events API
    ... and a handy dandy debugging GET endpoint
    """
    def get(self):
        return {"Status": "Not broken!"}

    def post(self):
        # Verify request
        # TODO: Implement signing in testing so we can get rid
        #   of this first conditional
        if not BLUEPRINT.config['TESTING']:
            if not verify_request():
                abort(403)

        # Get the json
        try:
            rjson = request.get_json()
        # TODO: Handle
        except Exception as e:
            raise e

        # Handle verification
        if is_verification_handshake(rjson):
            log.debug("Responding with verification challenge")
            return {"challenge": request.json['challenge']}
        log.debug("Parsing request, dispatching routing task")

        # Iter through rule list, if the callback matches queue
        # the associated task. 1 per request, so prioritize in the
        # list ordering
        for entry in rule_list:
            # Be paranoid, log excptions, but don't let one task break all the others
            try:
                if entry[0](rjson):
                    entry[1].delay(rjson)
                    break
            except Exception as e:
                log.exception(e)
                continue

        # Ack - slack wants a confirmation we got the message,
        # regardless of if we actually act on it.
        resp = Response()
        resp.statuts_code = 200
        log.debug("Ack-ing the request")
        return resp


class Version(Resource):
    def get(self):
        return {"version": __version__}


@BLUEPRINT.record
def handle_configs(setup_state):
    app = setup_state.app
    # Copy the app config (with env vars) into the blueprints config
    BLUEPRINT.config.update(app.config)

    # Primarily for testing, useful if you don't want to necessitate
    # the presence of certain vars in testing, or don't want to setup
    # some connections if implementation a DB or the like.
    if BLUEPRINT.config.get('DEFER_CONFIG'):
        log.debug("DEFER_CONFIG set, skipping configuration")
        return

    if BLUEPRINT.config.get("VERBOSITY"):
        log.debug("Setting verbosity to {}".format(str(BLUEPRINT.config['VERBOSITY'])))
        logging.basicConfig(level=BLUEPRINT.config['VERBOSITY'])
    else:
        log.debug("No verbosity option set, defaulting to WARN")
        logging.basicConfig(level="WARN")


API.add_resource(Root, "/")
API.add_resource(Version, "/version")
