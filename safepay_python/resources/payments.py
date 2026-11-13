import requests

from safepay_python.utils.builder import build_api_url
from safepay_python.utils.validation import validate_payment_details


class Payments:
    """Legacy ``/order/v1/init`` payment creation (deprecated)."""

    def __init__(self, config):
        self.config = config

    def create_payment(self, payment_details):
        validate_payment_details(payment_details)
        base_url = build_api_url(self.config['environment'])
        data = {
            'amount': payment_details['amount'],
            'client': self.config['apiKey'],
            'currency': payment_details['currency'],
            'environment': self.config['environment'],
        }
        response = requests.post(url=f"{base_url}/order/v1/init", json=data, timeout=30,
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'text/plain'})
        return response.json()
