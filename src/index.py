from utils.builder import *
from utils.validation import *
from resources.checkout import *
from resources.payments import *

class Safepay:
    def __init__(self, config):
        validate_options(config)
        self.config = config

    def get_checkout_url(self, checkout_details):
        checkout = Checkout(self.config)
        return checkout.create_checkout(checkout_details)

    async def set_payment_details(self, payment_details):
        payment = Payments(self.config)
        return await payment.create_payment(payment_details)

    def is_signature_valid(self, signature_body):
        verify = Verify(self.config)
        return verify.signature(signature_body)
    
    def is_webhook_valid(self, webhook_body):
        verify = Verify(self.config)
        return verify.webhook(webhook_body)

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
