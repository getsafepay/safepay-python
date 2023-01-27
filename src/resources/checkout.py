from utils.builder import *
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Checkout:
    def __init__(self, checkoutDetails, config):
        self.checkoutDetails = checkoutDetails
        self.config = config

    def createCheckout(self):
        # checkoutDetails["environment"] = config["environment"]
        url = buildCheckoutUrl(self.config["environment"])
        params = urllib.parse.urlencode({'beacon': self.checkoutDetails['beacon'],
                                         'cancel_url': self.checkoutDetails['cancelUrl'],
                                         'env': self.config["environment"],
                                         'order_id': self.checkoutDetails['orderId'],
                                         'redirect_url': self.checkoutDetails['redirectUrl'],
                                         'source': 'custom',
                                         'webhooks': str(self.checkoutDetails['webhooks'])})
        url += f'?{params}'
        # parsed_url = urlparse(url)
        # captured_value = parse_qs(parsed_url.query)['redirect_url'][0]

        # print(captured_value)

        return url
