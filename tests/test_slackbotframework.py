import unittest
import json
from os import environ
from os import urandom

# Defer configs
environ['SBF_DEFER_CONFIG'] = "True"
environ['SBF_CELERY_BROKER'] = "localhost"

import slackbotframework


slackbotframework.app.config['DEBUG'] = True
slackbotframework.app.config['TESTING'] = True
slackbotframework.app.config['SECRET_KEY'] = str(urandom(32))

slackbotframework.blueprint.BLUEPRINT.config['DEBUG'] = True
slackbotframework.blueprint.BLUEPRINT.config['TESTING'] = True
slackbotframework.blueprint.BLUEPRINT.config['SECRET_KEY'] = \
    slackbotframework.app.config['SECRET_KEY']
slackbotframework.blueprint.BLUEPRINT.config['VERIFICATION_TOKEN'] = "abc123"


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = slackbotframework.app.test_client()

    def tearDown(self):
        del self.app

    def testPass(self):
        self.assertEqual(True, True)

    def testVersionAvailable(self):
        x = getattr(slackbotframework, "__version__", None)
        self.assertTrue(x is not None)

    def testVersion(self):
        version_response = self.app.get("/version")
        self.assertEqual(version_response.status_code, 200)
        version_json = json.loads(version_response.data.decode())
        api_reported_version = version_json['version']
        self.assertEqual(
            slackbotframework.blueprint.__version__,
            api_reported_version
        )

    def testUrlVerificationHandshake(self):
        challenge_response = self.app.post(
            "/",
            json={
                "token": "abc123",
                "challenge": "def456",
                "type": "url_verification"
            }
        )
        self.assertEqual(challenge_response.status_code, 200)
        challenge_response_json = json.loads(challenge_response.data.decode())
        self.assertEqual(challenge_response_json['challenge'], "def456")


if __name__ == "__main__":
    unittest.main()
