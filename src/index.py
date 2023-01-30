from utils.builder import *
from utils.validation import *
from resources.checkout import *
from resources.payments import *
from resources.verify import *


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
