from utils.builder import *
from utils.validation import *

# # Testting all checkout and api urls

# print(buildCheckoutUrl("production"))
# print(buildCheckoutUrl("sandbox"))
# print(buildCheckoutUrl("development"))

# print(buildApiUrl("production"))
# print(buildApiUrl("sandbox"))
# print(buildApiUrl("development"))

print(validateOptions({
    'environment': 'sandbox',
    'apiKey': 'sec_asd12-2342s-1231s',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
}))

# obj = {'environment': 'sandbox',
#        'apiKey': 'sec_asd12-2342s-1231s',
#        'v1Secret': 'bar',
#        'webhookSecret': 'foo'}

# print(obj['apiKey'])
