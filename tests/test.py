import sys
sys.path.append("..")
from safepay_python.safepay import *
import asyncio
from tests.constants import *



# Object creation test

env = Safepay({
    'environment': ENVIRONMENT_DEVELOPMENT,
    'apiKey': TEST_DEVELOPMENT_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

env2 = Safepay({
    'environment': ENVIRONMENT_SANDBOX,
    'apiKey': TEST_SANDBOX_API_KEY,
    'v1Secret': TEST_V1_SECRET_KEY,
    'webhookSecret': TEST_WEBHOOK_SECRET_KEY
})

print(f'environment: {env.config}')
print(f'environment: {env2.config}')


# Payment test

payment_response = env.set_payment_details({'amount': 10000,
                                                'currency': 'PKR'})


print(f'paymentResponse: {payment_response}')

token = (payment_response['data'])['token']

print(f'token: {token}')

# Checkout url test

checkout_url = env.get_checkout_url({'beacon': TOKEN,
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': True})

print(f'checkoutURL: {checkout_url}')


# Verification test for signatures

verification_response = env.is_signature_valid({'sig': TEST_SIGNATURE,
                                                'tracker': TOKEN})

print(f'signature verification response: {verification_response}')

# Verification test for webhooks

wh_verification_response = env.is_webhook_valid({'x-sfpy-signature': TEST_WEBHOOK_SIGNATURE
                                                 },
                                                {'data': TEST_WEBHOOK_DATA})

print(f'webhook verification response: {wh_verification_response}')



