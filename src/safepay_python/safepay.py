from safepay_python.utils.builder import *
from safepay_python.utils.validation import *
from safepay_python.resources.checkout import *
from safepay_python.resources.payments import *
from safepay_python.resources.verify import *
import asyncio


class Safepay:
    def __init__(self, config):
        validate_options(config)
        self.config = config

    def get_checkout_url(self, checkout_details):
        checkout = Checkout(self.config)
        validate_checkout_parameters(checkout_details)
        return checkout.create_checkout(checkout_details)

    def set_payment_details(self, payment_details):

        async def paymentFucntion(payment_details):
            payment = Payments(self.config)
            value = await payment.create_payment(payment_details)
            return value

        payment_value = asyncio.run(paymentFucntion(payment_details))
        return payment_value

    def is_signature_valid(self, signature_body):
        verify = Verify(self.config)
        return verify.signature(signature_body)

    def is_webhook_valid(self, webhook_header, webhook_body):
        verify = Verify(self.config)
        return verify.webhook(webhook_header, webhook_body)