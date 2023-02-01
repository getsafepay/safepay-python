from Crypto.Hash import SHA256, SHA512
from Crypto.Hash import HMAC, SHA256
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

        # comptuted_sig = mac

        # print(comptuted_sig)

        # print(comptuted_sig == h.hexdigest())

        # h = HMAC.new(bytes(secret, encoding='utf-8'), digestmod=SHA256)
        # print(h)
        # h.update(bytes(tracker, encoding='utf-8'))
        # print(h.hexdigest())

        # secret = b'Swordfish'
        # h = HMAC.new(secret, digestmod=SHA256)
        # h.update(b'Hello')
        # print(h.hexdigest())

        # hash = SHA256.new(self.config['v1Secret'])
        # hash.update(tracker)
        # hash.digest('hex')

        #
        # return secret == sig

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

# Fatima's

# signature = (header['x-sfpy-signature'])
# print(f'sig: {signature}')
# stringifiedData = json.dumps(
#     body['data'], separators=(',', ':'))
# print(f'data: {stringifiedData}')
# a = bytearray(stringifiedData, 'utf-8')
# m = memoryview(a)
# print(m)
# secret = self.config['v1Secret']
# h = HMAC.new(bytes(secret, encoding='utf-8'), digestmod=SHA512)
# print(h)
# h.update(m)
# print(h.hexdigest())
# return signature == h

# Saeed's

# data = bytes(memoryview(json.dumps(
#     body['data'], separators=(',', ':'))).encode())
# print(data)
# signature = ['x-sfpy-signature']

# hash = SHA512.new(self.config.webhookSecret)
# hash.update(data)
# hash.digest('hex')
# return signature == h
