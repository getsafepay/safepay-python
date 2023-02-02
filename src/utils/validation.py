def validate_options(options):

    try:
        options['environment']
    except:
        raise Exception('Environment is missing')

    if validate_environment(options['environment']) == False:
        raise Exception('Environment is invalid')

    try:
        options['apiKey']
    except:
        raise Exception(f"API key is missing for {options['environment']}")

    try:
        options['v1Secret']
    except:
        raise Exception(f"v1 secret is missing for {options['environment']}")

    try:
        options['webhookSecret']
    except:
        raise Exception(
            f"Webhook secret is missing for {options['environment']}")

    return True


def validate_environment(env):

    if env in ["production", "sandbox", "development"]:
        return True
    else:
        return False


def validate_checkout_parameters(params):
    print(f'params: {params}')

    try:
        params['beacon']
    except:
        raise Exception(f"Token is missing")

    try:
        params['cancelUrl']
    except:
        raise Exception(f"Cancel url is missing")

    try:
        params['redirectUrl']
    except:
        raise Exception(f"Redirect url is missing")

    return True
