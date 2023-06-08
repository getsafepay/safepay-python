import sys
sys.path.append("..")
from safepay_python.safepay import *

ENVIRONMENT_SANDBOX = 'sandbox'
ENVIRONMENT_PRODUCTION = 'production'
ENVIRONMENT_DEVELOPMENT = 'development'
TEST_SANDBOX_API_KEY = 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5'
TEST_DEVELOPMENT_API_KEY = 'sec_5fe1bafa-23d9-4dd6-b9f5-3e122ea9f240'
TEST_V1_SECRET_KEY = 'd928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825'
TEST_WEBHOOK_SECRET_KEY = 'be0001c975bbfd4f78fa3af9e8a3aeae14aab420c859f2255e12f532028a38f5'
TOKEN = 'track_9511f95d-2c77-4fc7-9474-0dcca462f09a'
TEST_SIGNATURE = '50f339f5d9a28ece5f72a5dc208972fe468d3898427a54b6ed7df9be7c406b09'
TEST_WEBHOOK_SIGNATURE = '4898e402f404bdac76752d48a6d175de67971b1890d302982360dd2c5806a16106c705b1c68eee2f731d73cdae4aa515efc6ade54953efc19e88325914d740dc'
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


envSandbox = Safepay({
    'environment': ENVIRONMENT_SANDBOX,
    'apiKey': TEST_SANDBOX_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

envDevlopment = Safepay({
    'environment': ENVIRONMENT_DEVELOPMENT,
    'apiKey': TEST_DEVELOPMENT_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

envProduction = Safepay({
    'environment': ENVIRONMENT_PRODUCTION,
    'apiKey': TEST_SANDBOX_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})


