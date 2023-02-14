import json
from hashlib import sha256, sha512
import hmac
from safepay_python.utils.secure_compare import *


class Verify:
    def __init__(self, config):
        self.config = config

    def signature(self, body):
        signature = body['sig']
        tracker = body['tracker']
        secret = self.config['v1Secret']
        mac = hmac.new(secret.encode('utf-8'),
                       msg=tracker.encode('utf-8'),
                       digestmod=sha256)
        comptuted_sig = mac.hexdigest()
        comparison_res = secure_compare(signature, comptuted_sig)

        return comparison_res

    def webhook(self, header, body):
        signature = (header['x-sfpy-signature'])
        secret = self.config['webhookSecret']
        payload = json.dumps(
            body['data'], separators=(',', ':'))

        mac = hmac.new(secret.encode('utf-8'),
                       msg=payload.encode('utf-8'),
                       digestmod=sha512)
        comptuted_sig = mac.hexdigest()
        comparison_res = secure_compare(comptuted_sig, signature)
        
        return comparison_res
