from index import *
import asyncio

env = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
})
print(f'environment: {env.config}')

checkout_url = env.get_checkout_url({'beacon': '1234',
                                  'cancelUrl': 'http://example.com/cancel',
                                  'orderId': 'T800',
                                  'redirectUrl': 'http://example.com/success',
                                  'source': 'custom',
                                  'webhooks': str(True)})
print(f'checkoutURL: {checkout_url}')

payment_response = asyncio.run(env.set_payment_details({'amount': 10000,
                                                     'currency': 'PKR'}))
print(f'paymentResponse: {payment_response}')
