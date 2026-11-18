"""End-to-end sandbox check for the Express Checkout flow.

Creates a real sandbox payment session and auth token, prints the Checkout
URL, and checks the auth token's shape. Open the printed URL in a browser:
the Safepay checkout page should load with the amount below.

    SAFEPAY_SECRET_KEY=... SAFEPAY_API_KEY=sec_... python examples/sandbox_smoke_test.py
"""

import os
import sys

from safepay_python import APIError, SafepayClient

client = SafepayClient(
    secret_key=os.environ["SAFEPAY_SECRET_KEY"],
    api_key=os.environ["SAFEPAY_API_KEY"],
    environment="sandbox",
)

try:
    session = client.create_payment_session(10000, "PKR", metadata={"order_id": "smoke-test"})
    tracker = session["tracker"]["token"]
    print("tracker:", tracker, "| state:", session["tracker"]["state"])

    # Raw response, to confirm `data` is a bare string
    raw = client._session.post(
        client.api_base + "/client/passport/v1/token",
        headers={"X-SFPY-MERCHANT-SECRET": client.secret_key},
        timeout=client.timeout,
    ).json()
    print("passport `data` type:", type(raw.get("data")).__name__)

    tbt = client.create_auth_token()
    url = client.get_checkout_url(
        tracker, tbt,
        redirect_url="https://example.com/order/complete",
        cancel_url="https://example.com/order/cancel",
        order_id="smoke-test",
    )
    print("\nOpen this URL; the PKR 100.00 checkout page should load:\n" + url)
    print("\npaid yet:", client.is_paid(tracker))
except APIError as e:
    print("Safepay API error:", e.status_code, e.errors or e.body)
    sys.exit(1)
