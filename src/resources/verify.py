from Crypto.Hash import SHA256
from Crypto.Hash import SHA512
import json


class Verify:
    def __init__(self, config):
        self.config = config

    def signature(self, request):
        sig = request.body['sig']
        tracker = request.body['tracker']
        hash = SHA256.new(self.config.v1Secret)
        hash.update(tracker)
        hash.digest('hex')

        return sig == hash

    def webhook(self, request):
        data = memoryview(json.dumps(
            request.body['data'], separators=(',', ':')))
        signature = ['x-sfpy-signature']

        hash = SHA512.new(self.config.webhookSecret)
        hash.update(data)
        hash.digest('hex')

        return signature == hash
