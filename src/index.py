from utils.builder import *
from utils.validation import *
from resources.checkout import *

# # Testting all checkout and api urls

# print(buildCheckoutUrl("production"))
# print(buildCheckoutUrl("sandbox"))
# print(buildCheckoutUrl("development"))

# print(buildApiUrl("production"))
# print(buildApiUrl("sandbox"))
# print(buildApiUrl("development"))


class Safepay:
    def __init__(self, config):
        validateOptions(config)
        self.config = config


env1 = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_asd12-2342s-1231s',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
})


print(env1.config)

checkout1 = Checkout.createCheckout({'beacon': '1234',
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': str(True)}, env1.config)


print(checkout1)
