"""Safepay Express Checkout client."""

from urllib.parse import quote, urlencode

import requests

from safepay_python import webhooks
from safepay_python.errors import APIConnectionError, APIError, SafepayError

ENVIRONMENTS = {
    # environment: (API base URL, Checkout base URL)
    "production": ("https://api.getsafepay.com", "https://getsafepay.com"),
    "sandbox": ("https://sandbox.api.getsafepay.com", "https://sandbox.api.getsafepay.com"),
    "development": ("https://dev.api.getsafepay.com", "https://dev.api.getsafepay.com"),
}

DEFAULT_TIMEOUT = 30


class SafepayClient:
    """Server-side client for Safepay Express Checkout.

    Args:
        secret_key: your secret key, sent as ``X-SFPY-MERCHANT-SECRET``.
        api_key: your API key (``sec_...``), sent as ``merchant_api_key``
            when creating payment sessions.
        webhook_secret: your endpoint's shared secret, used to verify webhooks.
        environment: ``"sandbox"`` (default), ``"production"`` or ``"development"``.
        timeout: request timeout in seconds.
        session: optional ``requests.Session`` to reuse (proxies, retries...).

    Every API method returns the ``data`` field of Safepay's response and
    raises :class:`APIError` for non-2xx responses.
    """

    def __init__(self, secret_key, api_key=None, webhook_secret=None,
                 environment="sandbox", timeout=DEFAULT_TIMEOUT, session=None):
        if not secret_key:
            raise SafepayError("secret_key is required")
        if environment not in ENVIRONMENTS:
            raise SafepayError(
                "environment must be one of: %s" % ", ".join(sorted(ENVIRONMENTS))
            )
        self.secret_key = secret_key
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self.environment = environment
        self.api_base, self.checkout_base = ENVIRONMENTS[environment]
        self.timeout = timeout
        self._session = session or requests.Session()

    # ------------------------------------------------------------------ HTTP

    def _request(self, method, path, json=None):
        url = self.api_base + path
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-SFPY-MERCHANT-SECRET": self.secret_key,
        }
        try:
            resp = self._session.request(method, url, json=json, headers=headers,
                                         timeout=self.timeout)
        except requests.RequestException as exc:
            raise APIConnectionError("Could not reach Safepay: %s" % exc) from exc

        try:
            body = resp.json()
        except ValueError:
            body = resp.text

        if not 200 <= resp.status_code < 300:
            errors = []
            if isinstance(body, dict):
                errors = (body.get("status") or {}).get("errors") or []
            message = "; ".join(str(e) for e in errors) or (
                "Safepay API returned HTTP %d" % resp.status_code
            )
            raise APIError(message, status_code=resp.status_code, errors=errors, body=body)

        if not isinstance(body, dict) or "data" not in body:
            raise APIError("Unexpected response from Safepay", status_code=resp.status_code,
                           body=body)
        return body["data"]

    # ------------------------------------------------------------- Customers

    def create_customer(self, first_name, last_name, email, phone_number,
                        country="PK", is_guest=True):
        """Create a customer to prefill the checkout form. Returns the customer
        object; pass its ``token`` (``cus_...``) to :meth:`create_payment_session`
        and :meth:`get_checkout_url`."""
        return self._request("POST", "/user/customers/v1/", json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "country": country,
            "is_guest": is_guest,
        })

    # -------------------------------------------------------------- Payments

    def create_payment_session(self, amount, currency, intent="CYBERSOURCE",
                               mode="payment", entry_mode=None, customer=None,
                               metadata=None, include_fees=False, **extra):
        """Create a payment session (tracker) with ``POST /order/payments/v3/``.

        Args:
            amount: amount in the lowest denomination (PKR 100.00 -> 10000).
            currency: e.g. ``"PKR"`` or ``"USD"``.
            intent: ``"CYBERSOURCE"`` (default) or ``"MPGS"``.
            mode: payment flow, default ``"payment"``.
            entry_mode: e.g. ``"raw"``.
            customer: customer token (``cus_...``) to attach.
            metadata: dict stored on the payment, e.g. ``{"order_id": "T800"}``.
            include_fees: pass the MDR on to the shopper.
            **extra: any other field accepted by the endpoint.

        Returns the ``data`` object; the tracker token is
        ``result["tracker"]["token"]``.
        """
        if not self.api_key:
            raise SafepayError("api_key is required to create a payment session")
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 1:
            raise SafepayError("amount must be a positive integer in the lowest denomination")

        payload = {
            "merchant_api_key": self.api_key,
            "intent": intent,
            "mode": mode,
            "currency": currency,
            "amount": amount,
            "include_fees": include_fees,
        }
        if entry_mode:
            payload["entry_mode"] = entry_mode
        if customer:
            payload["user"] = customer
        if metadata:
            payload["metadata"] = metadata
        payload.update(extra)
        return self._request("POST", "/order/payments/v3/", json=payload)

    def create_auth_token(self):
        """Create a short-lived (1 hour) authentication token (TBT) with
        ``POST /client/passport/v1/token``. Returns the token string."""
        return self._request("POST", "/client/passport/v1/token")

    def get_checkout_url(self, tracker, tbt, redirect_url, cancel_url,
                         source="hosted", order_id=None, customer=None):
        """Build the Hosted Checkout URL. Makes no network request.

        Args:
            tracker: tracker token from :meth:`create_payment_session`.
            tbt: token from :meth:`create_auth_token`.
            redirect_url: where the shopper lands after paying.
            cancel_url: where the shopper lands after cancelling.
            source: ``"hosted"`` for websites, ``"mobile"`` for WebViews.
            order_id: your internal order id (optional).
            customer: customer token to prefill the form (optional).
        """
        for name, value in (("tracker", tracker), ("tbt", tbt),
                            ("redirect_url", redirect_url), ("cancel_url", cancel_url)):
            if not value:
                raise SafepayError("%s is required" % name)

        params = {
            "tbt": tbt,
            "tracker": tracker,
            "environment": self.environment,
            "source": source,
            "redirect_url": redirect_url,
            "cancel_url": cancel_url,
        }
        if order_id is not None:
            params["order_id"] = str(order_id)
        if customer:
            params["user_id"] = customer
        return "%s/embedded/?%s" % (self.checkout_base, urlencode(params))

    def create_checkout(self, amount, currency, redirect_url, cancel_url,
                        order_id=None, customer=None, source="hosted", metadata=None,
                        **session_options):
        """Convenience wrapper: create a payment session and an auth token,
        then build the Checkout URL.

        ``order_id`` is also stored in the payment's metadata so it comes back
        in webhooks. Returns ``{"tracker": "track_...", "url": "https://..."}``.
        """
        metadata = dict(metadata or {})
        if order_id is not None:
            metadata.setdefault("order_id", str(order_id))

        session = self.create_payment_session(amount, currency, customer=customer,
                                              metadata=metadata or None, **session_options)
        tracker = session["tracker"]["token"]
        tbt = self.create_auth_token()
        url = self.get_checkout_url(tracker, tbt, redirect_url, cancel_url,
                                    source=source, order_id=order_id, customer=customer)
        return {"tracker": tracker, "url": url}

    def fetch_payment(self, tracker):
        """Fetch a payment with ``GET /reporter/api/v1/payments/{tracker}``.
        ``result["tracker"]["state"] == "TRACKER_ENDED"`` means it was paid."""
        if not tracker:
            raise SafepayError("tracker is required")
        return self._request("GET", "/reporter/api/v1/payments/%s" % quote(tracker, safe=""))

    def is_paid(self, tracker):
        """True if the payment's tracker state is ``TRACKER_ENDED``."""
        return self.fetch_payment(tracker).get("tracker", {}).get("state") == "TRACKER_ENDED"

    # -------------------------------------------------------------- Webhooks

    def verify_webhook(self, payload, signature):
        """True if ``signature`` (the ``X-SFPY-SIGNATURE`` header) is valid for
        the raw request body ``payload``."""
        return webhooks.verify_signature(payload, signature, self._require_webhook_secret())

    def construct_webhook_event(self, payload, signature):
        """Verify a webhook and return the parsed event.

        Raises :class:`SignatureVerificationError` if the signature is invalid.
        """
        return webhooks.construct_event(payload, signature, self._require_webhook_secret())

    def _require_webhook_secret(self):
        if not self.webhook_secret:
            raise SafepayError("webhook_secret is required to verify webhooks")
        return self.webhook_secret
