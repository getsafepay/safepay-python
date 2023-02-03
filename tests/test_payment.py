import unittest
import sys
sys.path.append("..")
from src.index import *
from constants import *
import asyncio


class TestPaymentAPI(unittest.TestCase):

    def test_amount_missing(self):
        asyncio.run(envSandbox.set_payment_details({'currency': 'PKR'}))

    def test_currency_missing(self):
        asyncio.run(envSandbox.set_payment_details({'amount': 10000}))

    def test_function_not_async(self):
        envSandbox.set_payment_details({  'amount': 10000,
                                          'currency': 'PKR'})

    def test_sandbox_payment(self):
        asyncio.run(envSandbox.set_payment_details({  'amount': 10000,
                                          'currency': 'PKR'}))

    def test_development_payment(self):
        asyncio.run(envDevlopment.set_payment_details({ 'amount': 10000,
                                            'currency': 'PKR'}))
        
    def test_production_payment(self):
        asyncio.run(envProduction.set_payment_details({ 'amount': 10000,
                                            'currency': 'PKR'}))


if __name__ == '__main__':
    unittest.main()


