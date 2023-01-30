from utils.builder import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests


class Payments:
    def __init__(self, config):
        self.config = config

    async def createPayment(self, paymentDetails):
        baseUrl = buildApiUrl(self.config['environment'])
        url = '/order/v1/init'
        data = {
            'amount': paymentDetails['amount'],
            'client': self.config['apiKey'],
            'currency': paymentDetails['currency'],
            'environment': self.config['environment']
        }
        # headers are not required
        response = requests.post(url=f"{baseUrl}{url}", json=data, headers={
                                 'Content-type': 'application/json', 'Accept': 'text/plain'})

        return response.json()
