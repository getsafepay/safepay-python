def validateOptions(options):

    try:
        options['environment']

    except:
        raise Exception('Environment is missing')

    if validateEnvironment(options['environment']) == False:
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


def validateEnvironment(env):

    if env in ["production", "sandbox", "development"]:
        return True
    else:
        return False
