from safepay_python.utils.constants import *


def build_checkout_url(env):
    if env == Environment.Development.value:
        return CHECKOUT_DEVELOPMENT
    elif env == Environment.Sandbox.value:
        return CHECKOUT_SANDBOX
    else:
        return CHECKOUT_PRODUCTION


def build_api_url(env):
    if env == Environment.Development.value:
        return API_URL_DEVELOPMENT
    elif env == Environment.Sandbox.value:
        return API_URL_SANDBOX
    else:
        return API_URL_PRODUCTION
