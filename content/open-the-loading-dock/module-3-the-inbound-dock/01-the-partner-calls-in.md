# The Partner Calls In

**Story so far:** GlidePort can now *ask* the van partner for status (outbound, authenticated). But asking a hundred times a day is wasteful and slow. When a van actually delivers something, the partner should just **tell** GlidePort. That means opening a door the partner can knock on — an **inbound** endpoint.

## Push Beats Pull for Events

| | Outbound polling | Inbound event |
| --- | --- | --- |
| "Van delivered at 14:02" reaches GlidePort… | Up to the next poll interval | Immediately |
| Load on the partner | Every poll, forever | One call per event |
| GlidePort needs | A caller | A **listener** |

For events — delivered, failed delivery, address changed — **inbound is the right shape**.

## What "Inbound" Looks Like

The partner's system makes an HTTP call **to GlidePort**:

```
POST https://<instance>.service-now.com/api/now/van/events
Content-Type: application/json
X-Api-Key: •••••

{ "event": "delivered", "tracking": "GP123", "at": "2026-10-12T14:02:00Z" }
```

On GlidePort's side, something must **receive** that call and do something useful. Your options:

| Receiver | Built with | Notes |
| --- | --- | --- |
| **Scripted REST API** | Server-side script (see *Build Your Own API*) | Full control of path/verb/response |
| **OOB REST API** | Existing table APIs | Fast if the payload matches a table |
| **Webhook endpoint** | A Scripted REST resource | Common pattern for partner events |

You already know how to *build* a Scripted REST resource from *Build Your Own API*. Here the concern is the **integration pattern**, not the syntax.

## Pattern 1 — Do the Work Later

The single most important inbound rule: **respond fast, process asynchronously.**

The partner's system is waiting on you. If your handler runs a heavy chain (update order → recalc → notify → call another API), you hold their call open for seconds. Instead:

```
1. Validate + authenticate the request
2. Store the event (write a row / queue an event)
3. Return 202 Accepted immediately
4. Let a flow/job pick it up and do the real work
```

```js
(function process(request, response) {
    var body = request.body.data;

    // 2. record the raw event for later processing
    var gr = new GlideRecord('u_van_event');
    gr.initialize();
    gr.setValue('u_payload', JSON.stringify(body));
    gr.setValue('u_received_at', new GlideDateTime());
    gr.insert();

    // 3. acknowledge and stop
    response.setStatus(202);
    response.setBody(JSON.stringify({ received: true }));
})(request, response);
```

This also **decouples** you: if the partner slows down or retries, you stay responsive.

## Pattern 2 — Authenticate the Caller

An open endpoint is an open door. The partner must prove who they are, just as you did outbound:

| Method | How |
| --- | --- |
| **API key header** | Check a header against a stored credential |
| **Basic auth** | Verify `Authorization: Basic …` |
| **OAuth token** | Validate a bearer token / scope |
| **Mutual TLS** | Client certificate — strongest |

Reject anything unauthenticated with `401`. Never trust the payload just because the URL is "secret" — URLs leak.

```js
if (!request.getHeader('X-Api-Key') || request.getHeader('X-Api-Key') !== gs.getProperty('x_glideport.van_api_key')) {
    response.setStatus(401);
    response.setBody(JSON.stringify({ error: 'unauthorized' }));
    return;
}
```

## Pattern 3 — Be Idempotent

Networks retry. The partner might send the *same* "delivered" event twice. If your handler blindly inserts, you get duplicates. Use a **correlation id** in the payload:

```js
var eventId = body.event_id;                       // unique per event from the partner
var existing = new GlideRecord('u_van_event');
if (existing.get('u_event_id', eventId)) {
    response.setStatus(200);                        // already processed — acknowledge, do nothing
    response.setBody(JSON.stringify({ duplicate: true }));
    return;
}
```

**Process each event id once.** This is the inbound twin of the outbound idempotency key.

## Pattern 4 — Validate, Then Reject Loudly

```js
if (!body.tracking || !body.event) {
    response.setStatus(400);
    response.setBody(JSON.stringify({ error: 'tracking and event are required' }));
    return;
}
```

Return `400` for bad payloads so the partner's logs show it and they can fix their side — silence is the worst response to bad data.

## The Inbound Checklist

| Step | Why |
| --- | --- |
| Authenticate | Reject unknown callers |
| Validate payload | Bad data in = bad data everywhere |
| De-dupe by event id | Networks retry |
| Store, then `202` | Stay fast; decouple the work |
| Process asynchronously | Heavy work off the request path |
| Log every received event | Reconstruct what happened |

## Lab: Open a Door for "Delivered" Events

1. Create a Scripted REST resource `POST van/events` (recap *Build Your Own API*).
2. Require an `X-Api-Key` header; reject others with `401`.
3. Validate that `tracking` and `event` are present, else `400`.
4. De-dupe by `event_id`; store the raw payload in a staging table; return `202`.
5. From a test client (Postman/`curl`), send the same event twice and confirm exactly one row is stored the first time and a "duplicate" is acknowledged the second.

**Check your work:** unauthenticated → `401`; malformed → `400`; valid → `202` and one stored event; repeat → acknowledged, not duplicated.

## Key Takeaways

- Use **inbound events** for things that happen in real time; keep polling for bulk/legacy.
- **Respond fast, process late** — authenticate, validate, store, return `202`.
- **Authenticate** every inbound call — an open endpoint is an open door.
- Be **idempotent** with a correlation/event id; networks retry.
- **Validate and reject loudly** with `400` so partners can fix bad payloads.

## Best Practices

- Never do heavy processing in the request handler — hand off to a flow/job.
- Log the raw inbound payload before you transform it.
- Version your endpoint path (`/v1/van/events`) so you can change it later.
- Return meaningful status codes and small JSON bodies.
