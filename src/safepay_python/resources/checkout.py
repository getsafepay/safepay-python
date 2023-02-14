from safepay_python.utils.builder import *
import urllib.parse

class Checkout:
    def __init__(self, config):
        self.config = config

    def create_checkout(self, checkout_details):
        url = build_checkout_url(self.config["environment"])
        params = urllib.parse.urlencode({'beacon': checkout_details['beacon'],
                                         'cancel_url': checkout_details['cancelUrl'],
                                         'env': self.config["environment"],
                                         'order_id': checkout_details['orderId'],
                                         'redirect_url': checkout_details['redirectUrl'],
                                         'source': checkout_details['source'] if 'source' in checkout_details else 'custom',
                                         'webhooks': 'true' if ('webhooks' in checkout_details and checkout_details['webhooks'] == True) else 'false'})
        url += f'?{params}'
        return url

