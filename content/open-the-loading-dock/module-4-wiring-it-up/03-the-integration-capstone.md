# The Integration Capstone

**Story so far:** Every wire GlidePort needs now has a home: outbound calls, auth, inbound events, batch imports, spokes, and monitoring. Let me show you the whole dock wired end-to-end, then you'll build it.

## The GlidePort Integration

One order, one journey, every mechanism:

```
CUSTOMER PLACES ORDER
        │
        ▼
[ Flow: Automate the Delivery Line ]  (inbound trigger)
        │
        ├─ Outbound: POST https://dummyjson.com/carts/add   (book a van)
        │        auth: OAuth via alias "shipping-api"
        │        body: { userId, products: [ … ] }
        │        Try/Catch → on failure: task + alert
        │
        ├─ Store the partner's booking id on the order
        │
        └─ Spoke/REST step: post "new booking" to the dispatch channel

LATER, THE VAN PARTNER SENDS EVENTS
        │
        ▼
[ Inbound: POST /van/events ]  (authenticate → validate → de-dupe → 202)
        │
        └─ store event → flow: update order status; if delivered → close + notify

EVERY MORNING
        │
        ▼
[ Batch: 06:00 Load Data → Transform ]
        │        CSV manifest → import set → coalesce into orders
        └─ reconcile: mark orders missing from the manifest as "at risk"

ALWAYS
        │
        ▼
[ Monitoring: outbound HTTP log · import run history · flow executions ]
        └─ failures → logged + assigned task; success counters + heartbeat
```

Read that list again — every line is something you built in this course.

## The Design Decisions (and Why)

| Decision | Choice | Because |
| --- | --- | --- |
| Booking a van | **Outbound** call | GlidePort initiates; no user involved → **client credentials** |
| Status updates | **Inbound** events | Real-time, one call per event, push beats poll |
| Daily manifest | **Batch** import set | Bulk + scheduled; partner offers a CSV |
| Secrets | **Alias** `shipping-api` | Portable across environments, rotatable |
| Failure handling | **Try/Catch + task** | Failures must be visible and owned |
| Common systems | **Spoke** action if available | Don't hand-roll what's prebuilt |

No mechanism is "the" answer — each fits its **freshness and volume** need.

## The Trust Checklist

Before you call an integration done:

- [ ] **Authenticated** — outbound uses an alias; inbound rejects unknown callers.
- [ ] **No secrets in code** — credentials/aliases only.
- [ ] **Idempotent** — event ids dedupe; writes use idempotency keys; imports coalesce.
- [ ] **Bounded** — retries capped with backoff; `4xx` not retried.
- [ ] **Observable** — every call logged; failures create a task.
- [ ] **Resilient** — a partner outage degrades gracefully, doesn't lose the order.
- [ ] **Portable** — dev/test/prod differ only by alias binding.

## Lab: Wire the Whole Dock (Capstone)

Build the end-to-end integration in stages, testing each:

1. **Outbound booking.** Extend your delivery flow to call `POST https://dummyjson.com/carts/add` (the sandbox's "book a van"), authenticated via the `shipping-api` alias. Wrap it in Try/Catch.
2. **Store the result.** Save the returned cart `id` (your booking id) on the order; post a message to dispatch (spoke or REST step — `https://httpbin.org/post` works if you have no spoke).
3. **Inbound events.** Stand up `POST /van/events` (authenticate → validate → de-dupe → `202`), and a flow that updates the order and closes it on `delivered`.
4. **Batch reconcile.** Build the CSV → import set → transform with coalesce; schedule Load + Transform at 06:00; flag orders missing from the manifest.
5. **Observe.** Break the partner URL on purpose (e.g. point it at `https://httpbin.org/status/500`); confirm the failure is logged *and* a task is created. Add a success counter and a heartbeat.

**Verify end-to-end:**
- Create an order → booking call goes out → `booking_id` stored (check the outbound HTTP log).
- POST the same "delivered" event twice → one status update (check the staging table).
- Re-run the manifest import twice → same record count (coalesce).
- Break the partner → a task appears with the order number.

**Check your work:** the whole journey works, and every failure path is visible in logs with a human owner.

## Course Wrap-Up

You began with an island and ended with a connected dock. GlidePort now **calls out** (outbound REST), **proves who it is** (credentials, OAuth, aliases), **listens** (inbound events, de-duped and authenticated), **ingests bulk** (import sets with coalesce), **reuses prebuilt blocks** (spokes/REST steps), and **watches every wire** (logs, retries, alerts).

**Integrations connect the platform to the world. Next in the GlidePort arc: surfacing it — a customer-facing portal where people place and track their own deliveries.**

## Key Takeaways

- Real integrations combine **outbound, inbound, and batch** — each for its own need.
- **Aliases** make the whole thing portable and rotatable.
- **Idempotency** and **coalesce** are what make retries and re-runs safe.
- **Observability** turns a silent outage into an owned task.
- Design for the **bad day**: expire a token, break a URL, resend an event — and stay correct.
