from index import *
import asyncio
import requests

# Object creation test

env = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
    'v1Secret': 'd928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825',
    'webhookSecret': 'be0001c975bbfd4f78fa3af9e8a3aeae14aab420c859f2255e12f532028a38f5'
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

mac = hmac.new('d928d9b1d9e487957c6658be637621bbb104d64b6b436e86714c2ff3712bd825'.encode('utf-8'),
               msg=token.encode('utf-8'),
               digestmod=sha256)

sig = mac.hexdigest()

print(sig)

verification_response = env.is_signature_valid({'sig': sig,
                                                'tracker': token})

print(f'signature verification response: {verification_response}')

# Verification test for webhookss

# wh_verification_response = env.is_webhook_valid({'x-sfpy-signature':
#                                                  'ba4c442df5067b679f55919ebc282cb113e376d5a5e5d9c6655647d734823da75a4371759f921bce40963cb90505ed1f8c0405cb78257fd605d259d452a1a7c7'
#                                                  },
#                                                 {'data': {'client_id': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
#                                                           'created_at': '2021-09-29T12:00:40Z',
#                                                           'endpoint': 'http://127.0.0.1:9000',
#                                                           'notification': {
#                                                               'amount': '150',
#                                                               'currency': 'PKR',
#                                                               'fee': '4.92',
#                                                               'intent': 'PAYFAST',
#                                                               'metadata': {
#                                                                   'order_id': 'XG102312',
#                                                                   'source': 'shopify'
#                                                               },
#                                                               'net': '145.08',
#                                                               'state': 'PAID',
#                                                               'tracker': 'tracker_c5a5apsbcv41om3fg0u0',
#                                                               'user': 'johndoe@gmail.com'
#                                                           },
#                                                           'token': 'C5A5APSBCV41R2QF2MHG',
#                                                           'type': 'payment:created',
#                                                           'updated_at': '2021-09-29T12:00:40Z'}})

# print(f'webhook verification response: {wh_verification_response}')


# testing our python server

resp = requests.get(url="http://127.0.0.1:8000/my-first-api?name=Fatima")
print(resp.text)
