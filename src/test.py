from index import *
import asyncio
from utils.constants import *

# Object creation test

env = Safepay({
    'environment': ENVIRONMENT,
    'apiKey': TEST_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

print(f'environment: {env.config}')


# Payment test

payment_response = asyncio.run(env.set_payment_details({'amount': 10000,
                                                        'currency': 'PKR'}))

print(f'paymentResponse: {payment_response}')

# token = (payment_response['data'])['token']

# print(f'token: {token}')

# Checkout url test

checkout_url = env.get_checkout_url({'beacon': TOKEN,
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': 'true'})
print(f'checkoutURL: {checkout_url}')


# Verification test for signatures

# mac = hmac.new('d928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825'.encode('utf-8'),
#                msg=TOKEN.encode('utf-8'),
#                digestmod=sha256)

# sig = mac.hexdigest()

# print(sig)

verification_response = env.is_signature_valid({'sig': TEST_SIGNATURE,
                                                'tracker': TOKEN})

print(f'signature verification response: {verification_response}')

# Verification test for webhooks

wh_verification_response = env.is_webhook_valid({'x-sfpy-signature': TEST_WEBHOOK_SIGNATURE
                                                 },
                                                {'data': TEST_WEBHOOK_DATA})

print(f'webhook verification response: {wh_verification_response}')


# testing our python server

# resp = requests.get(url="http://127.0.0.1:8000/my-first-api?name=Fatima")
# print(resp.text)

# webhook = requests.post(url="http://127.0.0.1:8000/webhook",
#                         json={'name': 'fatima', 'age': 23}
#                         )

# print(webhook.json())
