import unittest
import sys
sys.path.append("..")
from src.index import *
from constants import *

class TestEnvironment(unittest.TestCase):

    def test_env_missing(self):
        Safepay({
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_wrong_env(self):
        Safepay({
            'environment': 'sadbox',
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_v1secret_missing(self):
        Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'apiKey': TEST_API_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_webhook_key_missing(self):
        Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
        })

    def test_api_key_missing(self):
        Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_env_sandbox(self):
        Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_env_development(self):
        Safepay({
            'environment': ENVIRONMENT_DEVELOPMENT,
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })

    def test_env_production(self):
        Safepay({
            'environment': ENVIRONMENT_PRODUCTION,
            'apiKey': TEST_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })


if __name__ == '__main__':
    unittest.main()


