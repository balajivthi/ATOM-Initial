# Every Way to Start

**Story so far:** Your welcome flow fires on *record created*. But GlidePort's day doesn't only begin when a customer clicks order — agents go on shift, vans fill up, overdue orders pile up at 5pm. Each moment has its own kind of starting gun. This lesson is the catalogue of triggers.

## The Trigger Is a Contract

A trigger answers two questions: **what event** starts the flow, and **what data** it hands you. Change the trigger and you change the flow's whole personality. You can only ever have one per flow.

## Record Triggers

The everyday workhorses. Choose a **table** and an **event**:

| Event | Fires when |
| --- | --- |
| **Created** | A new row is inserted |
| **Updated** | An existing row changes |
| **Created or Updated** | Either of the above |
| **Deleted** | A row is removed |

For GlidePort:

- *Created* → "A new order just arrived, greet the customer."
- *Updated* → "An order's status changed, tell the customer."
- *Deleted* → "An order was cancelled, release its van."

You can also scope the event to specific records with a **condition** (next lesson) and watch specific **fields** on updates.

## Scheduled Triggers

Not everything is caused by a record. Some work just *has* to happen on a clock:

| Trigger | Use it for |
| --- | --- |
| **Scheduled → Run once / Repeat** | Nightly cleanup, weekly reports |
| **Daily / Weekly / Monthly** | Recurring jobs with a start date |
| **On demand with a schedule** | A flow a user starts, that can also run on schedule |

GlidePort example: **every day at 17:00, find overdue orders and chase them.** No record change kicks this off — the *clock* does. A scheduled trigger hands the flow no `current` record; instead, you look records up with a **Look Up Records** action and loop with **For Each**.

## System & Integration Triggers

The platform can also begin a flow from outside a form:

| Trigger | Fires when |
| --- | --- |
| **Inbound Email** | A message lands in a configured mailbox (e.g. `orders@glideport.example`) |
| **REST** / **Webhook** | An external system posts to a flow URL |
| **Service Catalog** | A catalog item is ordered (record producer too) |
| **SLA** | A task's SLA timer starts, pauses, breaches, or completes |
| **Metric / KPI** | A metric threshold is crossed |

GlidePort example: a **webhook** fires when the van-tracking partner reports a delivery — that starts the "mark delivered and notify" flow, without anyone touching a record.

## Choosing a Trigger — A Cheat Sheet

| You want to… | Reach for… |
| --- | --- |
| React the moment a record appears | **Record → Created** |
| React to a change (and know the old value) | **Record → Updated** |
| Run on a clock, regardless of records | **Scheduled** |
| Let an external system push work in | **REST / Webhook** |
| Turn an email into an order | **Inbound Email** |
| Hand a flow to a user from a form or portal | **On demand / Catalog** |
| React to a deadline | **SLA** |

## One Event, One Data Shape

The trigger decides what pills you get:

- **Record trigger** → a `Record` pill (plus `Changed Fields` on update).
- **Scheduled trigger** → no record; you fetch your own.
- **Email trigger** → the message body, subject, sender.

Design tip: if a flow needs a record, a record trigger is usually the cleanest start. If it needs to *find* records, start scheduled and look them up.

## Lab: Pick the Right Starter

For each GlidePort need, decide the trigger without building it yet:

1. Greet a customer the instant an order is created → ?
2. Every morning at 06:00, rebuild the day's delivery plan → ?
3. When the van partner posts a "delivered" event, close the order → ?
4. When an order's `status` flips to `shipped`, email the tracking link → ?
5. Let a customer place an order from the portal → ?

**Check your work:**
1. Record → Created · 2. Scheduled (daily) · 3. REST/Webhook · 4. Record → Updated (condition on status) · 5. Service Catalog.

## Key Takeaways

- A trigger defines **both** the starting event and the data a flow receives.
- **Record** triggers cover created/updated/deleted; **Scheduled** covers the clock; **REST/Webhook/Email/Catalog/SLA** cover the outside world.
- Scheduled triggers hand you **no record** — look records up instead.
- Choose the trigger that naturally supplies the data the flow needs.

## Best Practices

- Match the trigger to the *cause*, not the convenience — a record trigger beats polling on a schedule when possible.
- Keep one trigger per flow; split unrelated starters into separate flows.
- For "on update" flows, watch the specific fields you care about.
- Prefer a webhook over a nightly re-scan when an external system can push.
