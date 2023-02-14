import unittest
import sys
sys.path.append("..")
from safepay_python.safepay import *
from constants import *

class TestEnvironment(unittest.TestCase):

    def test_env_missing(self):
        expectedException = "Environment is missing"
        try:
            Safepay({
                'apiKey': TEST_SANDBOX_API_KEY,
                'v1Secret': TEST_V1_SECRET_KEY,
                'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_wrong_env(self):
        expectedException = "Environment is invalid"
        try:
            Safepay({
            'environment': 'sadbox',
            'apiKey': TEST_SANDBOX_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)


    def test_v1secret_missing(self):
        expectedException = f"v1 secret is missing for {ENVIRONMENT_SANDBOX}"
        try:
             Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'apiKey': TEST_SANDBOX_API_KEY,
            'webhookSecret': TEST_WEBHOOK_SECRET_KEY
        })
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_webhook_key_missing(self):
        expectedException = f"Webhook secret is missing for {ENVIRONMENT_SANDBOX}"
        try:
            Safepay({
            'environment': ENVIRONMENT_SANDBOX,
            'apiKey': TEST_SANDBOX_API_KEY,
            'v1Secret': TEST_V1_SECRET_KEY,
        })
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_api_key_missing(self):
        expectedException = f"API key is missing for {ENVIRONMENT_SANDBOX}"
        try:
            Safepay({
                'environment': ENVIRONMENT_SANDBOX,
                'v1Secret': TEST_V1_SECRET_KEY,
                'webhookSecret': TEST_WEBHOOK_SECRET_KEY
            })
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_env_sandbox(self):
        actualResponse = Safepay({
                                'environment': ENVIRONMENT_SANDBOX,
                                'apiKey': TEST_SANDBOX_API_KEY,
                                'v1Secret': TEST_V1_SECRET_KEY,
                                'webhookSecret': TEST_WEBHOOK_SECRET_KEY
                            }).config

        expectedResponse = {'environment': 'sandbox', 'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5', 'v1Secret': 'd928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825', 'webhookSecret': 'be0001c975bbfd4f78fa3af9e8a3aeae14aab420c859f2255e12f532028a38f5'}
        self.assertEqual(actualResponse, expectedResponse)
        

    def test_env_development(self):
        actualResponse = Safepay({
                                    'environment': ENVIRONMENT_DEVELOPMENT,
                                    'apiKey': TEST_DEVELOPMENT_API_KEY,
                                    'v1Secret': TEST_V1_SECRET_KEY,
                                    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
                                }).config

        expectedResponse = {'environment': 'development', 'apiKey': 'sec_f99c1f23-c1d8-4b8e-a74a-5c0e01e1a106', 'v1Secret': 'd928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825', 'webhookSecret': 'be0001c975bbfd4f78fa3af9e8a3aeae14aab420c859f2255e12f532028a38f5'}
        self.assertEqual(actualResponse, expectedResponse)


if __name__ == '__main__':
    unittest.main()


