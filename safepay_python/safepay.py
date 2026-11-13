"""Legacy (0.0.6) interface — deprecated.

This class talks to Safepay's legacy checkout (``/order/v1/init`` and
``/checkout/pay``). It is kept so existing integrations do not break on
upgrade, but new code should use :class:`safepay_python.SafepayClient`,
which implements Express Checkout. It will be removed in 1.0.
"""

import warnings

from safepay_python.client import SafepayClient  # noqa: F401  (re-export)
from safepay_python.resources.checkout import Checkout
from safepay_python.resources.payments import Payments
from safepay_python.resources.verify import Verify
from safepay_python.utils.validation import validate_checkout_parameters, validate_options

_DEPRECATION = (
    "safepay_python.safepay.Safepay uses Safepay's legacy checkout and is deprecated; "
    "use safepay_python.SafepayClient (Express Checkout) instead. "
    "See the README section 'Migrating from 0.0.6'."
)


class Safepay:
    def __init__(self, config):
        warnings.warn(_DEPRECATION, DeprecationWarning, stacklevel=2)
        validate_options(config)
        self.config = config

    def get_checkout_url(self, checkout_details):
        validate_checkout_parameters(checkout_details)
        return Checkout(self.config).create_checkout(checkout_details)

    def set_payment_details(self, payment_details):
        return Payments(self.config).create_payment(payment_details)

    def is_signature_valid(self, signature_body):
        return Verify(self.config).signature(signature_body)

    def is_webhook_valid(self, webhook_header, webhook_body):
        return Verify(self.config).webhook(webhook_header, webhook_body)
