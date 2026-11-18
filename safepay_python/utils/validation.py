def validate_options(options):

    try:
        options['environment']
    except (KeyError, TypeError):
        raise Exception("Environment is missing")

    if validate_environment(options['environment']) == False:
        raise Exception("Environment is invalid")

    try:
        options['apiKey']
    except (KeyError, TypeError):
        raise Exception(f"API key is missing for {options['environment']}")

    try:
        options['v1Secret']
    except (KeyError, TypeError):
        raise Exception(f"v1 secret is missing for {options['environment']}")

    try:
        options['webhookSecret']
    except (KeyError, TypeError):
        raise Exception(
            f"Webhook secret is missing for {options['environment']}")

    return True


def validate_environment(env):

    if env in ["production", "sandbox", "development"]:
        return True
    else:
        return False


def validate_checkout_parameters(params):

    try:
        params['beacon']
    except (KeyError, TypeError):
        raise Exception(f"Token is missing")

    try:
        params['cancelUrl']
    except (KeyError, TypeError):
        raise Exception(f"Cancel url is missing")

    try:
        params['redirectUrl']
    except (KeyError, TypeError):
        raise Exception(f"Redirect url is missing")

    return True


def validate_payment_details(payment_details):

    try:
        payment_details['amount']
    except (KeyError, TypeError):
        raise Exception(f"Amount is missing")

    if payment_details['amount'] < 1:
        raise Exception(f"Amount should be greater than 0")

    try:
        payment_details['currency']
    except (KeyError, TypeError):
        raise Exception(f"Currency is missing")

    if validate_currency(payment_details['currency']) == False:
        raise Exception(f"Currency not supported")

    return True


def validate_currency(currency):

    if currency in ["PKR", "USD", "AED", "SAR", "CAD", "EUR", "GBP"]:
        return True
    else:
        return False
