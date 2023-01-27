from utils.builder import *
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Checkout:
    def __init__(self, config):
        # self.checkoutDetails = checkoutDetails
        self.config = config

    def createCheckout(self, checkoutDetails):
        url = buildCheckoutUrl(self.config["environment"])
        params = urllib.parse.urlencode({'beacon': checkoutDetails['beacon'],
                                         'cancel_url': checkoutDetails['cancelUrl'],
                                         'env': self.config["environment"],
                                         'order_id': checkoutDetails['orderId'],
                                         'redirect_url': checkoutDetails['redirectUrl'],
                                         'source': 'custom',
                                         'webhooks': str(checkoutDetails['webhooks'])})
        url += f'?{params}'
        # parsed_url = urlparse(url)
        # captured_value = parse_qs(parsed_url.query)['redirect_url'][0]

        # print(captured_value)

        return url
