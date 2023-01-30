from utils.constants import *


def buildCheckoutUrl(env):
    if env == Environment.Development.value:
        return CHECKOUT_DEVELOPMENT
    elif env == Environment.Sandbox.value:
        return CHECKOUT_SANDBOX
    else:
        return CHECKOUT_PRODUCTION


def buildApiUrl(env):
    if env == Environment.Development.value:
        return API_URL_DEVELOPMENT
    elif env == Environment.Sandbox.value:
        return API_URL_SANDBOX
    else:
        return API_URL_PRODUCTION
