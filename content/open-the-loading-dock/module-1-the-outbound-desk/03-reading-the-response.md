# Reading the Response

**Story so far:** GlidePort can now *make* an outbound call. But a call is worthless until you can read the answer — and partners answer in more ways than "yes." They return `404`s, rate-limit you, hand back half-filled JSON, and occasionally fall over. This lesson is about reading responses like a professional.

## The Response Object

`execute()` returns a response with everything you need to judge the call:

```js
var response = request.execute();

response.getStatusCode();     // 200, 404, 429, 500 ...
response.getBody();           // the raw text (usually JSON)
response.getHeaders();        // response headers
response.haveError();         // true if the HTTP call itself failed
response.getErrorMessage();   // why (connection/HTTP error)
response.getErrorCode();      // machine-readable error code
```

> **`haveError()` catches transport/HTTP failures, not application problems.** A `404` is a successful HTTP round-trip that *tells you* the parcel is unknown — handle both layers.

## Status Codes Are the Contract

| Range | Meaning | What to do |
| --- | --- | --- |
| `2xx` | Success | Parse the body and use it |
| `400` | Bad request | A bug in *your* payload — don't retry blindly; log and fix |
| `401` / `403` | Unauthorized / forbidden | Auth problem — check credentials/scope (Module 2) |
| `404` | Not found | The resource genuinely doesn't exist — handle, don't retry |
| `429` | Rate-limited | Wait (honor `Retry-After`) and retry — back off |
| `5xx` | Partner server error | Usually transient — retry with backoff, alert after N tries |

## Parsing the Payload

`getBody()` is a **string**. Turn it into usable data with `JSON.parse`, and guard against bad input:

```js
var response = request.execute();
var data = {};

if (response.getStatusCode() === 200) {
    try {
        data = JSON.parse(response.getBody());
    } catch (e) {
        gs.error('Partner returned non-JSON for ' + trackingNumber + ': ' + response.getBody());
        return null;
    }
    return data.status;   // e.g. "out_for_delivery"
}

if (response.getStatusCode() === 404) {
    gs.warn('Unknown tracking number: ' + trackingNumber);
    return 'unknown';
}

gs.error('Partner call failed (' + response.getStatusCode() + ') for ' + trackingNumber);
return null;
```

**Never** assume a field exists. `data.status` can be `undefined`; check before you write it to a record.

## Writing the Result Back

Once parsed, update GlidePort's own record — but only with good data:

```js
var partner = new DeliveryUtils().getTrackingStatus(order.getValue('u_tracking_number'));
if (partner && partner.status) {
    order.setValue('u_partner_status', partner.status);
    order.setValue('u_last_sync', new GlideDateTime());
    order.update();
}
```

## Retries and Backoff

Transient failures deserve a second chance — but not immediately, and not forever:

- **Retry** on `429` and `5xx`; **never** on `400`/`404`.
- **Back off** between tries (e.g. 2s, 4s, 8s) so you don't pile on a struggling partner.
- **Give up** after a few tries and **alert a human**.
- Use a **flow's Try/Catch + wait loop** (Module 4 here, and *Automate the Delivery Line*) or a **retry policy** on scheduled jobs.
- Respect `Retry-After` on `429`.

## Idempotency: Safe to Call Twice

If a call *changes* something on the partner's side (book a van, take a payment), a retry can accidentally do it twice. Guard with an **idempotency key** — a unique id for the operation, sent as a header, that the partner uses to recognise a repeat:

```js
request.setRequestHeader('Idempotency-Key', order.getValue('sys_id') + '-' + operation);
```

The partner ignores the second call with the same key and returns the first result. Design *outbound writes* this way.

## Logging: Leave a Trail

Outbound calls are recorded automatically — find them under **All → System Log → Outbound HTTP Requests** (`sys_outbound_http_log`). To make your own trail, log the essentials:

```js
gs.info('Shipping API: tracking=' + trackingNumber + ' status=' + response.getStatusCode());
```

Include the **partner**, the **resource id**, and the **status code** — enough to reconstruct what happened at 2am.

## Lab: Handle Every Answer

1. Extend `getTrackingStatus` to branch on the status code (`200` / `404` / `other`).
2. Parse JSON safely with a `try/catch`, and log a warning on non-JSON.
3. Update an order's `u_partner_status` only when the parse succeeded.
4. Simulate failures: point the endpoint at one that returns `404` and one that returns `500`; confirm each is handled without throwing.
5. Open **Outbound HTTP Requests** log and find your calls.

**Check your work:** `200` updates the order; `404` logs a warning and returns `unknown`; `5xx` logs an error; nothing throws an uncaught exception.

## Key Takeaways

- The response gives you a **status code**, a **body** (string), and error info.
- `haveError()` is about the *call*; the **status code** is about the *result*.
- **Parse defensively** — JSON can be malformed and fields can be missing.
- **Retry** transient failures (`429`/`5xx`) with backoff; never retry `400`/`404`.
- Use **idempotency keys** on writes, and **log** every call for observability.

## Best Practices

- Branch explicitly on `2xx` / `4xx` / `5xx` — don't treat every non-200 the same.
- Check the field you need exists before writing it to a record.
- Cap retries and alert rather than looping forever.
- Rely on the built-in **Outbound HTTP Request** log; add your own line for context.
