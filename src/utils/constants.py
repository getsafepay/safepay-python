from enum import Enum

ENVIRONMENT = 'sandbox'
TEST_API_KEY = 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5'
TEST_V1_SECRET_KEY = 'd928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825'
TEST_WEBHOOK_SECRET_KEY = 'be0001c975bbfd4f78fa3af9e8a3aeae14aab420c859f2255e12f532028a38f5'
TOKEN = 'track_9511f95d-2c77-4fc7-9474-0dcca462f09a'
TEST_SIGNATURE = '50f339f5d9a28ece5f72a5dc208972fe468d3898427a54b6ed7df9be7c406b09'
TEST_WEBHOOK_SIGNATURE = '910870282c2b040626293b8d7d2b3046cd14fc00225febf42efc05cf160eb391aca739470e368a0670dfab3877f4e7eda0da2ac760ca50017ac1b2ef971ada31'
TEST_WEBHOOK_DATA = {'client_id': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
                     'created_at': '2021-09-29T12:00:40Z',
                     'endpoint': 'http://127.0.0.1:9000',
                     'notification': {
                         'amount': '150',
                         'currency': 'PKR',
                         'fee': '4.92',
                         'intent': 'PAYFAST',
                         'metadata': {
                             'order_id': 'XG102312',
                             'source': 'shopify'
                         },
                         'net': '145.08',
                         'state': 'PAID',
                         'tracker': 'tracker_c5a5apsbcv41om3fg0u0',
                         'user': 'johndoe@gmail.com'
                     },
                     'token': 'C5A5APSBCV41R2QF2MHG',
                     'type': 'payment:created',
                     'updated_at': '2021-09-29T12:00:40Z'}

API_URL_PRODUCTION = 'https://api.getsafepay.com'
API_URL_SANDBOX = 'https://sandbox.api.getsafepay.com'
API_URL_DEVELOPMENT = 'https://dev.api.getsafepay.com'

CHECKOUT_PRODUCTION = 'https://getsafepay.com/checkout/pay'
CHECKOUT_SANDBOX = 'https://sandbox.api.getsafepay.com/checkout/pay'
CHECKOUT_DEVELOPMENT = 'https://dev.api.getsafepay.com/checkout/pay'


class Environment(Enum):
    Production = 'production'
    Sandbox = 'sandbox'
    Development = 'development'
