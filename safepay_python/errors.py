"""Exceptions raised by the Safepay client."""


class SafepayError(Exception):
    """Base class for every error raised by this library."""


class APIError(SafepayError):
    """Safepay returned a non-2xx response.

    Attributes:
        status_code: HTTP status code of the response.
        errors: the ``status.errors`` list from Safepay's response body, if any.
        body: the decoded response body (dict) or raw text when it is not JSON.
    """

    def __init__(self, message, status_code=None, errors=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors or []
        self.body = body


class APIConnectionError(SafepayError):
    """The request never got a response (DNS, timeout, connection reset...)."""


class SignatureVerificationError(SafepayError):
    """A webhook's ``X-SFPY-SIGNATURE`` did not match the payload."""
