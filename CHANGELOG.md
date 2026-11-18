# Changelog

## 0.1.0

### Added
- `SafepayClient`, a client for Safepay **Express Checkout**:
  - `create_payment_session()`: `POST /order/payments/v3/`
  - `create_auth_token()`: `POST /client/passport/v1/token`
  - `get_checkout_url()`: builds the `/embedded/` Hosted Checkout URL
  - `create_checkout()`: runs session, token and URL in one call
  - `fetch_payment()` / `is_paid()`: `GET /reporter/api/v1/payments/{tracker}`
  - `create_customer()`: prefill checkout with customer details
  - `verify_webhook()` / `construct_webhook_event()`: HMAC-SHA512 check of `X-SFPY-SIGNATURE`
- Typed errors: `SafepayError`, `APIError` (with `status_code`, `errors`, `body`), `APIConnectionError`, `SignatureVerificationError`.
- Request timeouts (30 s default) and support for passing your own `requests.Session`.
- Unit test suite.

### Changed
- Requires Python 3.8+.
- Dependencies loosened to `requests>=2.25,<3`. Pins on `urllib3` and `six` were removed.
- The legacy `Safepay.set_payment_details()` is now a plain synchronous call. It no longer drives an asyncio event loop, which broke on Python 3.12+ and inside async frameworks.

### Deprecated
- `safepay_python.safepay.Safepay` (the 0.0.6 legacy-checkout interface). It still works but emits a `DeprecationWarning`. It will be removed in 1.0.

### Fixed
- `pyproject.toml` pointed at `README.md`, but the file was `readme.md`, so builds failed on case-sensitive filesystems.
