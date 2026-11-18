"""Official Python library for the Safepay API (Express Checkout)."""

from safepay_python.client import SafepayClient
from safepay_python.errors import (
    APIConnectionError,
    APIError,
    SafepayError,
    SignatureVerificationError,
)
from safepay_python.webhooks import SIGNATURE_HEADER, construct_event, verify_signature

__version__ = "0.1.0"

__all__ = [
    "SafepayClient",
    "SafepayError",
    "APIError",
    "APIConnectionError",
    "SignatureVerificationError",
    "SIGNATURE_HEADER",
    "construct_event",
    "verify_signature",
    "__version__",
]
