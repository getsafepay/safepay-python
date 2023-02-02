import unittest
import sys
sys.path.append("..")
from src.index import *
from constants import *

class TestCheckoutUrl(unittest.TestCase):

    def test_token_missing(self):
        envSandbox.get_checkout_url({  'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': 'true'})

    def test_cancel_url_missing(self):
        envSandbox.get_checkout_url({  'beacon': TOKEN,
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': 'true'})

    def test_redirect_missing(self):
        envSandbox.get_checkout_url({  'beacon': TOKEN,
                                        'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'source': 'custom',
                                        'webhooks': 'true'})

    def test_sandbox_checkout_url(self):
        envSandbox.get_checkout_url({  'beacon': TOKEN,
                                        'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': 'true'})

    def test_development_checkout_url(self):
        envDevlopment.get_checkout_url({  'beacon': TOKEN,
                                        'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': 'true'})

    def test_production_checkout_url(self):
        envProduction.get_checkout_url({  'beacon': TOKEN,
                                        'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': 'true'})


if __name__ == '__main__':
    unittest.main()


