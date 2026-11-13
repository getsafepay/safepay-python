# Safepay Python SDK

Official Python library for Safepay **Express Checkout**. It runs on your server: you create a payment session, redirect the shopper to Safepay's Hosted Checkout page, and confirm the outcome when they come back.

> **Upgrading from 0.0.6?** 0.0.6 was built for Safepay's legacy checkout. Your existing code keeps working but now shows a `DeprecationWarning`. See [Migrating from 0.0.6](#migrating-from-006).

## How it works

1. The shopper clicks **Pay**. Your server creates a **payment session** (a [tracker](https://docs.getsafepay.com/concepts/tracker)) and a short-lived **authentication token**, then builds the **Checkout URL**.
2. You redirect the shopper to that URL and they pay on Safepay's Hosted Checkout.
3. Safepay sends the shopper back to your `redirect_url` with `?tracker=...` appended.
4. You confirm the payment by **fetching the tracker** and by handling the **`payment.succeeded` webhook**, then update the order.

## Installation

Requires Python 3.8 or later.

```bash
pip install --upgrade safepay-python
```

## Before you begin

- Create a sandbox account and [get your API keys](https://docs.getsafepay.com/developers/safepay/api-keys/):
  - **API key** (`sec_...`) identifies your account when you create payment sessions.
  - **Secret key** authenticates every server-side request (`X-SFPY-MERCHANT-SECRET`). Never expose it to the browser.
- [Set up a webhook endpoint](https://docs.getsafepay.com/developers/webhooks/overview/) and copy its **shared secret** from **Developers → Endpoints → View shared secret**.

## Configuration

```python
import os
from safepay_python import SafepayClient

safepay = SafepayClient(
    secret_key=os.environ["SAFEPAY_SECRET_KEY"],
    api_key=os.environ["SAFEPAY_API_KEY"],
    webhook_secret=os.environ["SAFEPAY_WEBHOOK_SECRET"],
    environment="sandbox",  # or "production"
)
```

| Option           | Required | Description |
| ---------------- | -------- | ----------- |
| `secret_key`     | Yes      | Your secret key. Sandbox and live keys are different. |
| `api_key`        | For payments | Your API key (`sec_...`). |
| `webhook_secret` | For webhooks | Your endpoint's shared secret. |
| `environment`    | No       | `sandbox` (default) or `production`. |
| `timeout`        | No       | Request timeout in seconds. Default `30`. |
| `session`        | No       | Your own `requests.Session` (proxies, retries). |

## Quick start

`create_checkout()` creates the payment session and the authentication token, and builds the Checkout URL, all in one call:

```python
checkout = safepay.create_checkout(
    amount=10000,          # PKR 100.00, in the lowest denomination
    currency="PKR",
    order_id="T800",       # your order id; also saved in metadata so it comes back in webhooks
    redirect_url="https://mywebsite.com/order/complete",
    cancel_url="https://mywebsite.com/order/cancel",
)

save_tracker_on_order("T800", checkout["tracker"])  # track_... — match webhooks with it
# redirect the shopper to checkout["url"]
```

The steps below do the same thing one call at a time. Use them when you need more control.

## Step 1: Create a payment session

```python
session = safepay.create_payment_session(
    amount=10000,
    currency="PKR",
    entry_mode="raw",
    metadata={"order_id": "T800"},
)
tracker = session["tracker"]["token"]  # track_...
```

| Parameter      | Required | Default        | Description |
| -------------- | -------- | -------------- | ----------- |
| `amount`       | Yes      |                | Integer in the **lowest denomination**. PKR 100.00 → `10000`. |
| `currency`     | Yes      |                | e.g. `PKR`, `USD`. |
| `intent`       | No       | `CYBERSOURCE`  | Payment channel: `CYBERSOURCE` or `MPGS`. |
| `mode`         | No       | `payment`      | See [payment modes](https://docs.getsafepay.com/concepts/payment-modes). |
| `entry_mode`   | No       |                | e.g. `raw`. See [entry modes](https://docs.getsafepay.com/concepts/payment-entry-modes). |
| `customer`     | No       |                | Customer token (`cus_...`) to prefill checkout. |
| `metadata`     | No       |                | Any dict, e.g. `{"order_id": "T800"}`. It comes back in webhooks. |
| `include_fees` | No       | `False`        | Pass the MDR on to the shopper. |

Example response (trimmed):

```json
{
  "tracker": {
    "token": "track_4f7d7e2d-ee05-44e3-81b7-6f6f2cca9727",
    "environment": "sandbox",
    "state": "TRACKER_STARTED",
    "intent": "CYBERSOURCE",
    "mode": "payment",
    "purchase_totals": { "quote_amount": { "currency": "PKR", "amount": 10000 } }
  },
  "capabilities": { "CYBERSOURCE": true }
}
```

## Step 2: Create an authentication token

```python
tbt = safepay.create_auth_token()
```

The token authenticates the Checkout page and **expires after 1 hour**. Once it expires, the shopper has to restart checkout from your store, so create a fresh token for each checkout attempt.

## Step 3: Generate the Checkout URL

```python
url = safepay.get_checkout_url(
    tracker=tracker,
    tbt=tbt,
    redirect_url="https://mywebsite.com/order/complete",
    cancel_url="https://mywebsite.com/order/cancel",
    order_id="T800",
)
# redirect the shopper to `url`
```

| Parameter      | Required | Default  | Description |
| -------------- | -------- | -------- | ----------- |
| `tracker`      | Yes      |          | `tracker.token` from Step 1. |
| `tbt`          | Yes      |          | Token from Step 2. |
| `redirect_url` | Yes      |          | Where the shopper lands after paying. |
| `cancel_url`   | Yes      |          | Where the shopper lands after cancelling. |
| `source`       | No       | `hosted` | `hosted` for websites, `mobile` for WebViews. |
| `order_id`     | No       |          | Your internal order id. |
| `customer`     | No       |          | Customer token to prefill the form. |

`get_checkout_url()` does not make a network request.

## Step 4: Show the outcome to the shopper

After paying, the shopper is redirected to:

```
https://mywebsite.com/order/complete?tracker=track_4f7d7e2d-ee05-44e3-81b7-6f6f2cca9727
```

Check the payment from your server:

```python
@app.get("/order/complete")
def order_complete():
    tracker = request.args["tracker"]
    if safepay.is_paid(tracker):           # tracker.state == "TRACKER_ENDED"
        return render_template("success.html")
    return render_template("pending.html")  # poll again, or wait for the webhook
```

`fetch_payment(tracker)` returns the full payment, including the tracker state and the payment method used. See [tracker states](https://docs.getsafepay.com/concepts/tracker-states/).

Use the redirect only to decide what to show the shopper. Fulfil the order from the webhook or from your own `fetch_payment()` call, never from query parameters.

## Step 5: Handle webhooks

Safepay sends `payment.succeeded` when a payment is captured and `payment.failed` when an attempt fails. Shoppers can retry on the Hosted Checkout page, so **the same tracker can produce several webhooks**. Make your handler idempotent.

Each webhook is signed with HMAC-SHA512 in the `X-SFPY-SIGNATURE` header. Pass the **raw request body** to the SDK, not parsed JSON:

```python
from flask import Flask, request
from safepay_python import SignatureVerificationError, SIGNATURE_HEADER

app = Flask(__name__)

@app.post("/webhooks/safepay")
def safepay_webhook():
    try:
        event = safepay.construct_webhook_event(
            request.get_data(),                      # raw bytes
            request.headers.get(SIGNATURE_HEADER, ""),
        )
    except SignatureVerificationError:
        return "invalid signature", 401

    if already_processed(event["token"]):            # evt_... — dedupe retries
        return "", 200

    data = event["data"]
    order_id = data.get("metadata", {}).get("order_id")

    if event["type"] == "payment.succeeded" and data["state"] == "TRACKER_ENDED":
        mark_order_paid(order_id, tracker=data["tracker"],
                        amount=data["amount"], currency=data["currency"])
    elif event["type"] == "payment.failed":
        record_failed_attempt(order_id, tracker=data["tracker"])

    mark_processed(event["token"])
    return "", 200
```

<details>
<summary>Django</summary>

```python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from safepay_python import SignatureVerificationError

@csrf_exempt
@require_POST
def safepay_webhook(request):
    try:
        event = safepay.construct_webhook_event(
            request.body, request.headers.get("X-SFPY-SIGNATURE", "")
        )
    except SignatureVerificationError:
        return HttpResponse(status=401)
    # ... handle event as above
    return HttpResponse(status=200)
```
</details>

<details>
<summary>FastAPI</summary>

```python
from fastapi import FastAPI, Request, HTTPException
from safepay_python import SignatureVerificationError

app = FastAPI()

@app.post("/webhooks/safepay")
async def safepay_webhook(request: Request):
    try:
        event = safepay.construct_webhook_event(
            await request.body(), request.headers.get("x-sfpy-signature", "")
        )
    except SignatureVerificationError:
        raise HTTPException(status_code=401)
    # ... handle event as above
    return {"ok": True}
```
</details>

Example `payment.succeeded` event:

```json
{
  "token": "evt_64b3218e-f65c-45a9-96b0-fe4e293bb879",
  "version": "2.0.0",
  "type": "payment.succeeded",
  "data": {
    "tracker": "track_06ee38cb-981d-4158-819f-7231f28314e4",
    "intent": "CYBERSOURCE",
    "state": "TRACKER_ENDED",
    "net": 43525,
    "fee": 1475,
    "amount": 45000,
    "currency": "PKR",
    "metadata": { "order_id": "AX-09u812312" },
    "charged_at": { "seconds": 1698754230, "nanos": 752997627 }
  }
}
```

Before marking an order paid, match `data.tracker` to the tracker you saved and check that `amount` and `currency` agree with the order. See [webhook types](https://docs.getsafepay.com/developers/webhooks/webhook-types/) for every event.

To check a signature without parsing the event, call `safepay.verify_webhook(raw_body, signature)`. It returns `True` or `False`.

## Optional: Prefill customer details

```python
customer = safepay.create_customer(
    first_name="Hassan",
    last_name="Zaidi",
    email="hzaidi@getsafepay.com",
    phone_number="+923331234567",
    country="PK",
)

checkout = safepay.create_checkout(
    amount=10000, currency="PKR", order_id="T800",
    customer=customer["token"],                # cus_...
    redirect_url="https://mywebsite.com/order/complete",
    cancel_url="https://mywebsite.com/order/cancel",
)
```

## Mobile apps (WebView)

Build the URL with `source="mobile"` and load it in a WebView. Close the WebView when its URL path changes to one of these:

| Outcome      | Path contains        |
| ------------ | -------------------- |
| Success      | `/external/complete` |
| Cancellation | `/external/error`    |

Then confirm the payment on your server with `is_paid()` or the webhook.

## Errors

```python
from safepay_python import APIError, APIConnectionError, SafepayError

try:
    checkout = safepay.create_checkout(...)
except APIError as e:            # Safepay returned a non-2xx response
    log.error("Safepay %s: %s", e.status_code, e.errors)
except APIConnectionError:       # network failure or timeout — safe to retry
    ...
except SafepayError:             # invalid arguments or configuration
    ...
```

## Test and go live

1. Test with Safepay's [test cards](https://docs.getsafepay.com/developers/safepay/test-cards/). Cover frictionless and step-up 3-D Secure, both successful and failed, and time-outs.
2. Check test payments in the sandbox Dashboard under **Payments → Payments 2.0**.
3. [Apply for a live account](https://getsafepay.com/dashboard/signup) and request the payment methods you need.
4. Set `environment="production"` and switch to your **live** API key, secret key and webhook secret.

## Migrating from 0.0.6

0.0.6 code still runs on 0.1.0 because the old `Safepay` class remains available. It shows a `DeprecationWarning` and will be removed in 1.0.

| 0.0.6 (legacy)                                                  | 0.1.0 (Express Checkout) |
| --------------------------------------------------------------- | ------------------------ |
| `from safepay_python.safepay import *`                          | `from safepay_python import SafepayClient` |
| `Safepay({"environment", "apiKey", "v1Secret", "webhookSecret"})` | `SafepayClient(secret_key=, api_key=, webhook_secret=, environment=)` |
| `set_payment_details({"amount", "currency"})` → `/order/v1/init` | `create_payment_session(amount, currency)` → `/order/payments/v3/` |
| No equivalent                                                   | `create_auth_token()` |
| `get_checkout_url({"beacon", "cancelUrl", "redirectUrl", ...})` → `/checkout/pay` | `get_checkout_url(tracker, tbt, redirect_url, cancel_url)` → `/embedded/` |
| `source` defaulted to `custom`                                  | `hosted`, or `mobile` for WebViews |
| `webhooks=True`                                                 | Removed. Webhooks are configured per endpoint in the Dashboard. |
| `is_signature_valid({"sig", "tracker"})` with `v1Secret`        | Removed. Use `is_paid(tracker)` and webhooks instead. |
| `is_webhook_valid(headers, body)`                               | `construct_webhook_event(raw_body, signature)` |

## Development

```bash
pip install -e . pytest
pytest
```
