import unittest
import sys
sys.path.append("..")
from safepay_python.safepay import *
from constants import *

class TestCheckoutUrl(unittest.TestCase):

    def test_token_missing(self):
        expectedException = "Token is missing"
        try:
            envSandbox.get_checkout_url({   'cancelUrl': 'http://example.com/cancel',
                                            'orderId': 'T800',
                                            'redirectUrl': 'http://example.com/success',
                                            'source': 'custom',
                                            'webhooks': True})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_cancel_url_missing(self):
        expectedException = "Cancel url is missing"
        try:
            envSandbox.get_checkout_url({   'beacon': TOKEN,
                                            'orderId': 'T800',
                                            'redirectUrl': 'http://example.com/success',
                                            'source': 'custom',
                                            'webhooks': True})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)


    def test_redirect_missing(self):
        expectedException = "Redirect url is missing"
        try:
            envSandbox.get_checkout_url({   'beacon': TOKEN,
                                            'cancelUrl': 'http://example.com/cancel',
                                            'orderId': 'T800',
                                            'source': 'custom',
                                            'webhooks': True})

        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_sandbox_checkout_url(self):
        expectedValue = "https://sandbox.api.getsafepay.com/checkout/pay?beacon=track_9511f95d-2c77-4fc7-9474-0dcca462f09a&cancel_url=http%3A%2F%2Fexample.com%2Fcancel&env=sandbox&order_id=T800&redirect_url=http%3A%2F%2Fexample.com%2Fsuccess&source=custom&webhooks=true"
        actualValue = envSandbox.get_checkout_url({ 'beacon': TOKEN,
                                                    'cancelUrl': 'http://example.com/cancel',
                                                    'orderId': 'T800',
                                                    'redirectUrl': 'http://example.com/success',
                                                    'source': 'custom',
                                                    'webhooks': True})

        self.assertEqual(actualValue, expectedValue)


    def test_development_checkout_url(self):
        expectedValue = "https://dev.api.getsafepay.com/checkout/pay?beacon=track_9511f95d-2c77-4fc7-9474-0dcca462f09a&cancel_url=http%3A%2F%2Fexample.com%2Fcancel&env=development&order_id=T800&redirect_url=http%3A%2F%2Fexample.com%2Fsuccess&source=custom&webhooks=true"
        actualValue = envDevlopment.get_checkout_url({ 'beacon': TOKEN,
                                                    'cancelUrl': 'http://example.com/cancel',
                                                    'orderId': 'T800',
                                                    'redirectUrl': 'http://example.com/success',
                                                    'source': 'custom',
                                                    'webhooks': True})

        self.assertEqual(actualValue, expectedValue)


if __name__ == '__main__':
    unittest.main()


