# Why Integrate

**Story so far:** GlidePort's Delivery App is smart (scripting) and self-driving (automation) — but it lives on an island. The van partner, the payments gateway, the address-validation service, and the customer's own systems all live *outside*. Orders still arrive by email, tracking numbers get copy-pasted, and the daily delivery plan is rebuilt by hand. Integration is how GlidePort stops being an island.

> **Practice Ground.** Every hands-on call in this course talks to something **real** — a free, public **partner sandbox** — so no lab ever asks you to imagine an answer. The endpoints, the one-time setup, and copy-paste `curl` checks live on the **[Lab Setup](/lab-setup)** page. Skim it once now; you'll return to it when a lab says *"call the partner"*.

## The Island Problem

Today, GlidePort is the only system that knows the whole story. Everyone else knows a fragment:

| System | Knows | GlidePort gets it by… |
| --- | --- | --- |
| Van partner | Where the van is right now | A person logging into their portal |
| Payments gateway | Whether the card cleared | A nightly emailed spreadsheet |
| Address service | Whether a postcode is real | Nobody checks — bad addresses just fail |
| Customer | When they'll get their parcel | An email a human writes |

Every one of those gaps is a manual bridge — slow, error-prone, and invisible.

## What Integration Actually Is

**Integration** is systems talking to each other directly, without a human in the middle. Instead of pasting tracking numbers into GlidePort, the van partner *tells* GlidePort. Instead of reading a spreadsheet, GlidePort *asks* the payments gateway.

The currency of that conversation is the **API** — an agreed set of URLs, requests, and responses.

## Two Directions

Every integration travels one of two ways:

| Direction | Name | Example |
| --- | --- | --- |
| GlidePort → them | **Outbound** | Call the van partner to book a pickup |
| Them → GlidePort | **Inbound** | Partner posts a "delivered" event to us |

Most real GlidePort flows use **both**: we call out to book a van (outbound), and the partner pushes status updates back (inbound).

## The Integration Map

```
                 ┌─────────────────────┐
                 │   Van partner API   │◀── outbound: book a pickup
                 │ (partner sandbox)   │──▶ inbound: delivered events
                 └─────────▲───────────┘
                           │
   ┌───────────────┐   ┌───┴────────────────┐   ┌──────────────────┐
   │ Payments      │◀──│   GlidePort         │──▶│ Address service  │
   │ gateway       │   │   Delivery App      │   │ (postcode check) │
   └───────────────┘   └───┬────────────────┘   └──────────────────┘
                           │
                 ┌─────────▼───────────┐
                 │ Nightly manifest    │◀── inbound: batch file import
                 │ (CSV import set)    │
                 └─────────────────────┘
```

Draw this map *before* you build anything — it's your checklist and your roadmap.

## The Vocabulary

| Term | Meaning |
| --- | --- |
| **Endpoint** | The URL you call (`https://dummyjson.com/carts/1`) |
| **Request / Response** | What you send, and what comes back |
| **Payload** | The body of a request or response, usually **JSON** |
| **Status code** | `200` OK, `201` created, `400` bad request, `401` unauthorized, `404` not found, `500` server error, `429` rate-limited |
| **Authentication** | How the other side knows *who* is calling |
| **Webhook** | A URL an external system calls to notify you of an event |
| **Poll vs push** | You ask repeatedly, vs they tell you when something happens |
| **Idempotency** | Doing the same call twice has the same effect as once |
| **Retry** | Trying again after a failure, with backoff |

## Poll vs Push — Pick Deliberately

| | **Poll** (you ask) | **Push / webhook** (they tell) |
| --- | --- | --- |
| Latency | As often as you ask | Near-instant |
| Load | You hammer them with requests | One call per event |
| Complexity | Simple to start | Needs an inbound endpoint + auth |
| Use when | No webhook offered, or data changes slowly | The partner offers events |

GlidePort: **push** for "the van just delivered" (instant), **poll or batch** for "give me today's full manifest" (rare, bulk).

## What "Done" Looks Like

An integration isn't finished when it works once. It's finished when it is:

- **Reliable** — retries transient failures and alerts on real ones.
- **Secure** — never hardcodes secrets; uses credentials and OAuth properly.
- **Observable** — every call is logged, so you can answer "did it work?"
- **Idempotent** — a duplicate delivery doesn't create a duplicate order update.

## Key Takeaways

- Systems on an island create manual bridges; **integration** removes the human.
- Integrations travel **outbound** (you call them) or **inbound** (they call you).
- The **integration map** is your plan: who talks to whom, in which direction.
- Choose **push** for events and **batch/poll** for bulk.
- A good integration is reliable, secure, observable, and idempotent — not just "working."
