import json
from hashlib import sha256, sha512
import hmac
from utils.secure_compare import *


class Verify:
    def __init__(self, config):
        self.config = config

    def signature(self, body):
        sig = body['sig']
        print(f'signature: {sig}')
        tracker = body['tracker']
        print(f'tracker: {tracker}')
        secret = self.config['v1Secret']
        print(f'secret: {secret}')

        # hashing method
        # mac = HMAC.new(bytes(secret, encoding='utf-8'), digestmod=SHA256)
        # print(mac)
        # mac.update(bytes(tracker, encoding='utf-8'))
        # print(f'after hashing: {mac.hexdigest()}')
        # digestedMac = mac.hexdigest()

        # Second hashing method
        mac = hmac.new(secret.encode('utf-8'),
                       msg=tracker.encode('utf-8'),
                       digestmod=sha256)

        digestedMac = mac.hexdigest()

        return sig == digestedMac

    def webhook(self, header, body):
        signature = (header['x-sfpy-signature'])
        print(f'signature: {signature}')
        secret = self.config['v1Secret']
        print(f'secret: {secret}')
        print(f"data: {body['data']}")
        payload = json.dumps(
            body['data'], separators=(',', ':'))
        print(f'payload: {payload}')

        mac = hmac.new(secret.encode('utf-8'),
                       msg=payload.encode('utf-8'),
                       digestmod=sha512)
        comptuted_sig = mac.hexdigest()
        print(f'computed sig: {comptuted_sig}')
        comparison_res = secure_compare(comptuted_sig, signature)
        print(f'comparison res: {comparison_res}')
        return comparison_res
