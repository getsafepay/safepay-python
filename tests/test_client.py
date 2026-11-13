import hashlib
import hmac
import json
import unittest
import warnings
from unittest import mock
from urllib.parse import parse_qs, urlparse

import requests

from safepay_python import (
    APIConnectionError,
    APIError,
    SafepayClient,
    SafepayError,
    SignatureVerificationError,
)


def fake_response(status=200, body=None, text=None):
    resp = mock.Mock()
    resp.status_code = status
    if body is not None:
        resp.json.return_value = body
        resp.text = json.dumps(body)
    else:
        resp.json.side_effect = ValueError("no json")
        resp.text = text or ""
    return resp


def make_client(**kw):
    session = mock.Mock(spec=requests.Session)
    opts = dict(secret_key="secret", api_key="sec_key", webhook_secret="whsec",
                environment="sandbox", session=session)
    opts.update(kw)
    return SafepayClient(**opts), session


class ConfigTests(unittest.TestCase):
    def test_requires_secret_key(self):
        with self.assertRaises(SafepayError):
            SafepayClient(secret_key="")

    def test_rejects_unknown_environment(self):
        with self.assertRaises(SafepayError):
            SafepayClient(secret_key="s", environment="staging")

    def test_production_urls(self):
        c = SafepayClient(secret_key="s", environment="production")
        self.assertEqual(c.api_base, "https://api.getsafepay.com")
        self.assertEqual(c.checkout_base, "https://getsafepay.com")


class PaymentSessionTests(unittest.TestCase):
    def test_create_payment_session_request(self):
        client, session = make_client()
        session.request.return_value = fake_response(201, {
            "data": {"tracker": {"token": "track_1", "state": "TRACKER_STARTED"}},
            "status": {"errors": [], "message": "success"},
        })
        data = client.create_payment_session(10000, "PKR", entry_mode="raw",
                                             customer="cus_1", metadata={"order_id": "T800"})
        self.assertEqual(data["tracker"]["token"], "track_1")

        method, url = session.request.call_args[0]
        kwargs = session.request.call_args[1]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "https://sandbox.api.getsafepay.com/order/payments/v3/")
        self.assertEqual(kwargs["headers"]["X-SFPY-MERCHANT-SECRET"], "secret")
        self.assertEqual(kwargs["json"], {
            "merchant_api_key": "sec_key", "intent": "CYBERSOURCE", "mode": "payment",
            "currency": "PKR", "amount": 10000, "include_fees": False,
            "entry_mode": "raw", "user": "cus_1", "metadata": {"order_id": "T800"},
        })

    def test_amount_must_be_positive_int(self):
        client, _ = make_client()
        for bad in (0, -5, 10.5, "100", True):
            with self.assertRaises(SafepayError):
                client.create_payment_session(bad, "PKR")

    def test_requires_api_key(self):
        client, _ = make_client(api_key=None)
        with self.assertRaises(SafepayError):
            client.create_payment_session(100, "PKR")

    def test_api_error_carries_details(self):
        client, session = make_client()
        session.request.return_value = fake_response(400, {
            "data": None, "status": {"errors": ["invalid currency"], "message": "error"},
        })
        with self.assertRaises(APIError) as ctx:
            client.create_payment_session(100, "XYZ")
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.errors, ["invalid currency"])
        self.assertIn("invalid currency", str(ctx.exception))

    def test_non_json_error(self):
        client, session = make_client()
        session.request.return_value = fake_response(502, text="Bad Gateway")
        with self.assertRaises(APIError) as ctx:
            client.create_auth_token()
        self.assertEqual(ctx.exception.body, "Bad Gateway")

    def test_connection_error(self):
        client, session = make_client()
        session.request.side_effect = requests.ConnectionError("boom")
        with self.assertRaises(APIConnectionError):
            client.create_auth_token()


class CheckoutTests(unittest.TestCase):
    def test_auth_token(self):
        client, session = make_client()
        session.request.return_value = fake_response(200, {"data": "tbt=="})
        self.assertEqual(client.create_auth_token(), "tbt==")
        self.assertEqual(session.request.call_args[0][1],
                         "https://sandbox.api.getsafepay.com/client/passport/v1/token")

    def test_checkout_url(self):
        client, _ = make_client()
        url = client.get_checkout_url("track_1", "a+b/c==", "https://shop.com/ok?x=1",
                                      "https://shop.com/cancel", order_id=42, customer="cus_9")
        parsed = urlparse(url)
        self.assertEqual(f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
                         "https://sandbox.api.getsafepay.com/embedded/")
        q = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        self.assertEqual(q, {
            "tbt": "a+b/c==", "tracker": "track_1", "environment": "sandbox",
            "source": "hosted", "redirect_url": "https://shop.com/ok?x=1",
            "cancel_url": "https://shop.com/cancel", "order_id": "42", "user_id": "cus_9",
        })

    def test_checkout_url_production_host(self):
        client, _ = make_client(environment="production")
        url = client.get_checkout_url("t", "b", "https://a", "https://c")
        self.assertTrue(url.startswith("https://getsafepay.com/embedded/?"))

    def test_checkout_url_requires_fields(self):
        client, _ = make_client()
        with self.assertRaises(SafepayError):
            client.get_checkout_url("track_1", "", "https://a", "https://c")

    def test_create_checkout(self):
        client, session = make_client()
        session.request.side_effect = [
            fake_response(201, {"data": {"tracker": {"token": "track_7"}}}),
            fake_response(200, {"data": "tbt7"}),
        ]
        out = client.create_checkout(5000, "PKR", "https://a/ok", "https://a/no", order_id="T1")
        self.assertEqual(out["tracker"], "track_7")
        self.assertIn("tracker=track_7", out["url"])
        self.assertIn("tbt=tbt7", out["url"])
        first_payload = session.request.call_args_list[0][1]["json"]
        self.assertEqual(first_payload["metadata"], {"order_id": "T1"})


class FetchTests(unittest.TestCase):
    def test_fetch_and_is_paid(self):
        client, session = make_client()
        session.request.return_value = fake_response(200, {
            "data": {"tracker": {"token": "track_1", "state": "TRACKER_ENDED"}},
        })
        self.assertTrue(client.is_paid("track_1"))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "https://sandbox.api.getsafepay.com/reporter/api/v1/payments/track_1")

    def test_not_paid(self):
        client, session = make_client()
        session.request.return_value = fake_response(200, {
            "data": {"tracker": {"state": "TRACKER_STARTED"}},
        })
        self.assertFalse(client.is_paid("track_1"))


class WebhookTests(unittest.TestCase):
    event = {"token": "evt_1", "type": "payment.succeeded",
             "endpoint": "https://shop.com/hook",
             "data": {"tracker": "track_1", "state": "TRACKER_ENDED", "amount": 45000}}

    def sig(self, raw, secret="whsec"):
        return hmac.new(secret.encode(), raw, hashlib.sha512).hexdigest()

    def test_raw_body_signature(self):
        client, _ = make_client()
        raw = json.dumps(self.event).encode()  # pretty-ish spacing
        self.assertTrue(client.verify_webhook(raw, self.sig(raw)))

    def test_compact_reencoded_signature(self):
        client, _ = make_client()
        compact = json.dumps(self.event, separators=(",", ":")).encode()
        spaced = json.dumps(self.event, indent=2).encode()
        self.assertTrue(client.verify_webhook(spaced, self.sig(compact)))

    def test_matches_php_json_encode_unescaped_slashes(self):
        # PHP json_encode(..., JSON_UNESCAPED_SLASHES) output for self.event
        php = ('{"token":"evt_1","type":"payment.succeeded","endpoint":"https://shop.com/hook",'
               '"data":{"tracker":"track_1","state":"TRACKER_ENDED","amount":45000}}').encode()
        client, _ = make_client()
        self.assertTrue(client.verify_webhook(json.dumps(self.event, indent=1), self.sig(php)))

    def test_dict_payload_accepted(self):
        client, _ = make_client()
        compact = json.dumps(self.event, separators=(",", ":")).encode()
        self.assertTrue(client.verify_webhook(self.event, self.sig(compact)))

    def test_bad_signature(self):
        client, _ = make_client()
        raw = json.dumps(self.event).encode()
        self.assertFalse(client.verify_webhook(raw, self.sig(raw, "other")))
        self.assertFalse(client.verify_webhook(raw, ""))
        self.assertFalse(client.verify_webhook(b"not json", "abc"))

    def test_construct_event(self):
        client, _ = make_client()
        raw = json.dumps(self.event).encode()
        self.assertEqual(client.construct_webhook_event(raw, self.sig(raw)), self.event)
        with self.assertRaises(SignatureVerificationError):
            client.construct_webhook_event(raw, "deadbeef")

    def test_requires_webhook_secret(self):
        client, _ = make_client(webhook_secret=None)
        with self.assertRaises(SafepayError):
            client.verify_webhook(b"{}", "x")


class LegacyTests(unittest.TestCase):
    config = {"environment": "sandbox", "apiKey": "sec_1", "v1Secret": "bar",
              "webhookSecret": "foo"}

    def test_old_import_path_still_works_with_warning(self):
        from safepay_python.safepay import Safepay
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            env = Safepay(self.config)
        self.assertTrue(any(issubclass(x.category, DeprecationWarning) for x in w))

        url = env.get_checkout_url({"beacon": "track_1", "cancelUrl": "https://c",
                                    "redirectUrl": "https://r", "orderId": "T800"})
        self.assertTrue(url.startswith("https://sandbox.api.getsafepay.com/checkout/pay?"))

        sig = hmac.new(b"bar", b"track_1", hashlib.sha256).hexdigest()
        self.assertTrue(env.is_signature_valid({"sig": sig, "tracker": "track_1"}))

    def test_legacy_payment_is_sync(self):
        from safepay_python.safepay import Safepay
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            env = Safepay(self.config)
        with mock.patch("safepay_python.resources.payments.requests.post") as post:
            post.return_value = fake_response(200, {"data": {"token": "track_x"}})
            out = env.set_payment_details({"amount": 100, "currency": "PKR"})
        self.assertEqual(out["data"]["token"], "track_x")


if __name__ == "__main__":
    unittest.main()
