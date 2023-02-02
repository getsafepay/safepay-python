from enum import Enum

API_URL_PRODUCTION = 'https://api.getsafepay.com'
API_URL_SANDBOX = 'https://sandbox.api.getsafepay.com'
API_URL_DEVELOPMENT = 'https://dev.api.getsafepay.com'

CHECKOUT_PRODUCTION = 'https://getsafepay.com/checkout/pay'
CHECKOUT_SANDBOX = 'https://sandbox.api.getsafepay.com/checkout/pay'
CHECKOUT_DEVELOPMENT = 'https://dev.api.getsafepay.com/checkout/pay'


class Environment(Enum):
    Production = 'production'
    Sandbox = 'sandbox'
    Development = 'development'
