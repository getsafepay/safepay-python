from index import *
import asyncio

# Object creation test

env = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
})

print(f'environment: {env.config}')


# Payment test

payment_response = asyncio.run(env.set_payment_details({'amount': 10000,
                                                        'currency': 'PKR'}))

print(f'paymentResponse: {payment_response}')

token = (payment_response['data'])['token']

print(f'token: {token}')

# Checkout url test

checkout_url = env.get_checkout_url({'beacon': token,
                                     'cancelUrl': 'http://example.com/cancel',
                                     'orderId': 'T800',
                                     'redirectUrl': 'http://example.com/success',
                                     'source': 'custom',
                                     'webhooks': str(True)})
print(f'checkoutURL: {checkout_url}')


# Verification test for signatures

# verification_response = env.is_signature_valid({'sig': '530fdbcf1bf498aff65e42faff0791c366b0794dbe2e7bc1681ba1837b0c7a25',
#                                                 'tracker': '1234'})

# print(f'verification response: {verification_response}')
