from utils.builder import *
from utils.validation import *

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
