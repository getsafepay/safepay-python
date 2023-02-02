import unittest
import sys
sys.path.append("..")
from src.index import *
from constants import *
import asyncio

env = Safepay({
    'environment': ENVIRONMENT,
    'apiKey': TEST_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

class TestPaymentAPI(unittest.TestCase):

    def test_amount_missing(self):
        asyncio.run(env.set_payment_details({'currency': 'PKR'}))

    def test_currency_missing(self):
        asyncio.run(env.set_payment_details({'amount': 10000}))

    def test_function_not_async(self):
        env.set_payment_details({   'amount': 10000,
                                    'currency': 'PKR'})

    def test_payment_okay(self):
        env.set_payment_details({  'amount': 10000,
                                    'currency': 'PKR'})


if __name__ == '__main__':
    unittest.main()


