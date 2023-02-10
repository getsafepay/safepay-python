# Safepay Python SDK

Official python library for [Safepay API](https://getsafepay.com).

## Installation

### With Pip

```
pip install @sfpy/python-sdk
```

## Usage

Import and create a Safepay client by passing your config;

```python
from "python-sdk" import Safepay;

safepay =  Safepay({
  'environment': 'sandbox',
  'apiKey': 'sec_asd12-2342s-1231s',
  'v1Secret': 'bar',
  'webhookSecret': 'foo',
})
```

You can now create payments and checkout links.

### Payments

#### Create payment

| Parameter  | Type         | Required |
| ---------- | ------------ | -------- |
| `amount`   | `number`     | Yes      |
| `currency` | `PKR`, `USD` | Yes      |

```python
payment_response = asyncio.run(safepay.set_payment_details({  'amount': 10000,
                                                              'currency': 'PKR'}))

token = (payment_response['data'])['token']

# Pass `token` to create checkout link
```

### Checkout

#### Create checkout link

| Parameter     | Type      | Description                                   | Required |
| ------------- | --------- | --------------------------------------------- | -------- |
| `token`       | `string`  | Token from `safepay.payments.create`          | Yes      |
| `orderId`     | `string`  | Your internal invoice / order id              | No       |
| `cancelUrl`   | `string`  | Url to redirect to if user cancels the flow   | Yes      |
| `redirectUrl` | `string`  | Url to redirect to if user completes the flow | Yes      |
| `source`      | `string`  | Optional, defaults to `custom`                | No       |
| `webhooks`    | `boolean` | Optional, defaults to `false`                 | No       |

```python
checkout_url = safepay.get_checkout_url({   'beacon': token,
                                            'cancelUrl': 'http://example.com/cancel',
                                            'orderId': 'T800',
                                            'redirectUrl': 'http://example.com/success',
                                            'source': 'custom',
                                            'webhooks': True})

# set webhooks = True if want to subscribe to webhooks
# redirect user to `url`
```

### Verification

#### Signature

| Parameter | Type     | Description                       | Required |
| --------- | -------- | --------------------------------- | -------- |
| `request` | `object` | The `req` object from your server | Yes      |

```python
signature_verification = safepay.is_signature_valid({   'sig': 'abcd',
                                                        'tracker': token })

# mark the invoice as paid if valid
# show an error if invalid
```

#### Webhook

| Parameter | Type     | Description                       | Required |
| --------- | -------- | --------------------------------- | -------- |
| `request` | `object` | The `req` object from your server | Yes      |

```python
webhook_verification = safepay.is_webhook_valid({'x-sfpy-signature': 'abcd'},
                                                {'data': data})

# mark the invoice as paid if valid
# show an error if invalid
```
