import unittest
import sys
sys.path.append("..")
from src.index import *
from constants import *

env = Safepay({
    'environment': ENVIRONMENT,
    'apiKey': TEST_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

class TestSum(unittest.TestCase):

    def test_token_missing(self):
        env.get_checkout_url({
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': 'true'})

    def test_cancel_url_env(self):
        env.get_checkout_url({'beacon': TOKEN,
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': 'true'})

    def test_redirect_missing(self):
        env.get_checkout_url({'beacon': TOKEN,
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'source': 'custom',
                                     'webhooks': 'true'})

    def test_params_checkout_url_okay(self):
        env.get_checkout_url({'beacon': TOKEN,
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': 'true'})


if __name__ == '__main__':
    unittest.main()


