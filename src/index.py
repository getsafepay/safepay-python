from utils.builder import *
from utils.validation import *
from resources.checkout import *
from resources.payments import *


class Safepay:
    def __init__(self, config):
        validateOptions(config)
        self.config = config

    def getCheckoutURL(self):
        checkout = Checkout(self.config)
        return checkout.createCheckout({'beacon': '1234',
                                        'cancelUrl': 'http://example.com/cancel',
                                        'orderId': 'T800',
                                        'redirectUrl': 'http://example.com/success',
                                        'source': 'custom',
                                        'webhooks': str(True)})

    async def setPaymentDetails(self):
        payment = Payments(self.config)
        return await payment.createPayment({'amount': 10000,
                                            'currency': 'PKR'})

        # env1 = Safepay({
        #     'environment': 'sandbox',
        #     'apiKey': 'sec_9286c6a3-a159-492d-9f72-dbe424517fb5',
        #     'v1Secret': 'bar',
        #     'webhookSecret': 'foo'
        # })

        # print(env1.config)

        # checkout1 = Checkout(env1.config)

        # print(checkout1.createCheckout({'beacon': '1234',
        #                                 'cancelUrl': 'http://example.com/cancel',
        #                                 'orderId': 'T800',
        #                                 'redirectUrl': 'http://example.com/success',
        #                                 'source': 'custom',
        #                                 'webhooks': str(True)}))

        # payment1 = Payments(env1.config)

        # async def main():
        #     # async_func()#this will do nothing because coroutine object is created but not awaited
        #     # await async_func()
        # print(await payment1.createPayment({'amount': 10000,
        #                                     'currency': 'PKR'}))

        # asyncio.run(main())
