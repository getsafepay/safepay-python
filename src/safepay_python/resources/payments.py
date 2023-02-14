from safepay_python.utils.builder import *
from safepay_python.utils.validation import *
import requests
import json


class Payments:
    def __init__(self, config):
        self.config = config

    async def create_payment(self, payment_details):
        validate_payment_details(payment_details)
        base_url = build_api_url(self.config['environment'])
        url = '/order/v1/init'
        data = {
            'amount': payment_details['amount'],
            'client': self.config['apiKey'],
            'currency': payment_details['currency'],
            'environment': self.config['environment']
        }

        response = requests.post(url=f"{base_url}{url}", json=data, headers={
                                 'Content-type': 'application/json', 'Accept': 'text/plain'})

        return response.json()
