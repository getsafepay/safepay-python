"""Webhook signature verification.

Safepay signs every webhook with HMAC-SHA512 using your endpoint's shared
secret and sends the hex digest in the ``X-SFPY-SIGNATURE`` header.
"""

import hashlib
import hmac
import json

from safepay_python.errors import SignatureVerificationError

SIGNATURE_HEADER = "X-SFPY-SIGNATURE"


def _sign(secret, message):
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha512).hexdigest()


def _to_bytes(payload):
    if isinstance(payload, (bytes, bytearray)):
        return bytes(payload)
    if isinstance(payload, str):
        return payload.encode("utf-8")
    # Already-parsed JSON (dict/list)
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def verify_signature(payload, signature, secret):
    """Return True if ``signature`` is valid for ``payload``.

    ``payload`` should be the raw request body (bytes or str). A parsed dict
    is accepted too, but the raw body is more reliable.

    The signature is checked against the raw body first, then against the
    compact JSON re-encoding of the payload (what Safepay's PHP reference
    implementation signs: ``json_encode($payload, JSON_UNESCAPED_SLASHES)``).
    """
    if not signature or not secret:
        return False
    signature = signature.strip().lower()

    raw = _to_bytes(payload)
    if hmac.compare_digest(_sign(secret, raw), signature):
        return True

    try:
        compact = json.dumps(json.loads(raw), separators=(",", ":")).encode("utf-8")
    except ValueError:
        return False
    if compact == raw:
        return False
    return hmac.compare_digest(_sign(secret, compact), signature)


def construct_event(payload, signature, secret):
    """Verify ``payload`` and return the parsed event dict.

    Raises:
        SignatureVerificationError: the signature is missing or invalid.
        ValueError: the payload is not valid JSON.
    """
    if not verify_signature(payload, signature, secret):
        raise SignatureVerificationError("Webhook signature verification failed")
    if isinstance(payload, (dict, list)):
        return payload
    return json.loads(_to_bytes(payload))
