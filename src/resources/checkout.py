from utils.builder import *
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs


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
                                         'source': 'custom',
                                         'webhooks': str(checkout_details['webhooks'])})
        url += f'?{params}'

        # parsed_url = urlparse(url)
        # captured_value = parse_qs(parsed_url.query)['redirect_url'][0]

        # print(captured_value)

        return url


# const transaction = {
#     token: "trans_123123234",
#     reference: 524523,
#     tracker: "track_1232342",
#     amount: 4000,
#     currency: "PKR",
#     fees: 100,
#     net: 3900,
#     sig: "123123123lk123"
# }

# const { sig, tracker } = transaction
# const safepay = new Safepay({
#     v1Secret: "123123jkh12lk3jh1jk23"
# })

# const isValid = safepay.verify.signature(tracker, sig)
