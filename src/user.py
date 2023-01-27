from index import *
import asyncio

env = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
})
print(env.config)

checkoutURL = env.getCheckoutURL({'beacon': '1234',
                                  'cancelUrl': 'http://example.com/cancel',
                                  'orderId': 'T800',
                                  'redirectUrl': 'http://example.com/success',
                                  'source': 'custom',
                                  'webhooks': str(True)})
print(checkoutURL)

paymentInfo = asyncio.run(env.setPaymentDetails({'amount': 10000,
                                                 'currency': 'PKR'}))
print(paymentInfo)
