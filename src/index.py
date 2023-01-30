from utils.builder import *
from utils.validation import *
from resources.checkout import *
from resources.payments import *


class Safepay:
    def __init__(self, config):
        validateOptions(config)
        self.config = config

    def getCheckoutURL(self, checkoutDetails):
        checkout = Checkout(self.config)
        return checkout.createCheckout(checkoutDetails)

    async def setPaymentDetails(self, paymentDetails):
        payment = Payments(self.config)
        return await payment.createPayment(paymentDetails)
