import hmac


def secure_compare(a, b):
    """Constant-time ``a == b`` for str or bytes (kept for backwards compatibility)."""
    if isinstance(a, str):
        a = a.encode('utf-8')
    if isinstance(b, str):
        b = b.encode('utf-8')
    return hmac.compare_digest(a, b)
