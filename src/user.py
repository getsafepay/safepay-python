from index import *
import asyncio

env = Safepay({
    'environment': 'sandbox',
    'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
    'v1Secret': 'bar',
    'webhookSecret': 'foo'
})
print(env.config)

checkoutURL = env.getCheckoutURL()
print(checkoutURL)

paymentDetails = asyncio.run(env.setPaymentDetails())
print(paymentDetails)
