import hmac
import six


def secure_compare(a, b):
    """
    Return 'a == b'.  This function uses an approach designed to prevent
    timing analysis, making it appropriate for cryptography.
    a and b must both be of the same type: either str (ASCII only),
    or any bytes-like object.
    """

    def utf8(value):
        if six.PY2 and isinstance(value, six.text_type):
            return value.encode('utf-8')
        else:
            return value

    return hmac.compare_digest(utf8(a), utf8(b))
