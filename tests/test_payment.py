import sys
sys.path.append("..")
import asyncio
from constants import *
from safepay_python.safepay import *
import unittest



class TestPaymentAPI(unittest.TestCase):

    def test_wrong_currency(self):
        expectedException = 'Currency not supported'
        try:
            envSandbox.set_payment_details({'amount': 1000, 'currency': 'JPY'})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_amount_missing(self):
        expectedException = 'Amount is missing'
        try:
            envSandbox.set_payment_details({'currency': 'PKR'})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_currency_missing(self):
        expectedException = 'Currency is missing'
        try:
            envSandbox.set_payment_details({'amount': 1000})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)

    def test_amount_less_than_zero(self):
        expectedException = 'Amount should be greater than 0'
        try:
            envSandbox.set_payment_details({'amount': -1, 'currency':'PKR'})
        except Exception as e:
            self.assertEqual(e.args[0], expectedException)


    def test_sandbox_payment(self):
        expectedResponse = {'errors': [], 'message': 'success'}
        actualResponse = envSandbox.set_payment_details({'amount': 10000, 'currency': 'PKR'})
        self.assertEqual(actualResponse['status'], expectedResponse)

    def test_development_payment(self):
        expectedResponse = {'errors': [], 'message': 'success'}
        actualResponse = envDevlopment.set_payment_details({'amount': 10000, 'currency': 'PKR'})
        self.assertEqual(actualResponse['status'], expectedResponse)



   

if __name__ == '__main__':
    unittest.main()
