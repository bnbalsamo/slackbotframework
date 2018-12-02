"""
Slack Bot Framework
"""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"


from flask import Flask, jsonify
from flask_env import MetaFlaskEnv
from .blueprint import BLUEPRINT
from .blueprint.exceptions import Error


class Configuration(metaclass=MetaFlaskEnv):
    """
    Pulls all environmental variables that being with 'SLACKY_' into the app
    config, which is then in turn copied into the blueprint config when it is
    registered.

    Note: The variable *must* be referenced here, or it won't be pulled from
    the environment.
    """
    ENV_PREFIX = 'SBF_'
    DEBUG = False
    DEFER_CONFIG = False
    SIGNING_SECRET = None
    BOT_OAUTH_TOKEN = None
    SECRET_KEY = None


app = Flask(__name__)


@app.errorhandler(Error)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.config.from_object(Configuration)

app.register_blueprint(BLUEPRINT)
