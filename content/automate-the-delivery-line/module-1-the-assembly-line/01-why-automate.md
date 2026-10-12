# Why Automate?

**Story so far:** GlidePort's Delivery App is live. Business Rules quietly set statuses, Client Scripts polish the forms, and Script Includes keep the logic tidy. Yet the team still burns an afternoon on the same sequence by hand: confirm the order, tell the nearest agent, book a van, email the customer a tracking link, then chase anything overdue. A rule reacts to *one* record at a time — it can't draw a whole journey. That's the job of **automation**, and on this platform it starts with the **flow**.

## The Problem With One-Record Thinking

Business Rules are fantastic at reflexes:

- "When an order is inserted, default the status."
- "After a record updates, fire an event."

But GlidePort's real work is a **journey**, not a reflex:

| Step | Who does it today |
| --- | --- |
| 1. Confirm the order | A human |
| 2. Assign the nearest agent | A human |
| 3. Book a delivery van | A human, in another tool |
| 4. Email the customer a tracking link | A human |
| 5. Chase orders that miss their window | A human, if they remember |

Every one of those steps is a place where work stalls, gets forgotten, or happens out of order. The platform can carry that load for us.

## What Is a Flow?

A **flow** is a multi-step automation you build on a visual canvas. You place a **trigger**, then stack **actions**, and add **logic** where the route branches. Behind every step is server-side code you never have to write.

```
  [ Trigger ] ─▶ [ Action ] ─▶ [ Action ] ─▶ ( done )
   when a        send the        create the
   record is     agent a         van-booking
   created       heads-up        task
```

Read it top-to-bottom like a shopping list, change one step without touching the others, and watch it run.

## Where Flow Designer Lives

**All → Process Automation → Flow Designer → New → Flow.**

Flows are stored in `sys_hub_flow` (and their pieces in a family of `sys_hub_*` tables). You build them with a drag-and-drop canvas — no IDE, no deployment script.

> **Naming note:** the tool is the *builder*; a **flow** is the artifact you build. One flow = one automation.

## The Anatomy of a Flow

| Piece | What it does |
| --- | --- |
| **Trigger** | What *starts* the flow (record created/updated, a schedule, an inbound email, a REST call…) |
| **Action** | One unit of work — send a notification, create a record, ask for approval, run a script, call a subflow |
| **Flow logic** | Controls the route: **If**, **For Each**, **Wait**, **Do Until**, **Parallel**, **Try/Catch** |
| **Data pill** | A draggable chip that pipes a value (the order's number, the agent's email) into a later step |
| **Stage** | A visual label that groups steps so a long flow reads like chapters |
| **Flow variable** | Named storage for a value you compute and reuse |

## A Flow at a Glance

Here's the first flow we'll build, described in English before a single click:

> **When an order is created →** send the customer a welcome email → stamp the order's status to `new` → log that we told them.

That's a trigger and two actions. Small, but it's the same skeleton every big flow grows from.

## Flow Designer vs Business Rules

| | **Business Rule** | **Flow Designer** |
| --- | --- | --- |
| **Best for** | One quick reaction on one table | A multi-step journey across tables and systems |
| **Who builds it** | Developer (writes script) | Admin / analyst (no code) |
| **Visibility** | Logic hidden in a script field | Visible steps, logged, easy to read |
| **Branching** | You write `if/else` by hand | Drag **If/Else**, **For Each**, **Wait** |
| **Approvals & timeouts** | Painful to build | Built-in actions |
| **Cost** | Server-side, always runs | Same, but runs on the async flow engine |

**Rule of thumb:** if you can describe it as *"when X happens, do A, then B, then C,"* reach for a flow. If it's *"the instant this record saves, tweak a field,"* a Business Rule is leaner.

## Why Teams Reach for Flows

- **Readable** — anyone on the team can open the canvas and see what happens.
- **Logged** — every run is recorded; you can replay a specific order and see each step.
- **Reusable** — package common work as subflows and custom actions.
- **Safe to change** — reorder a step without rewriting server code.

## Key Takeaways

- Business Rules reflex on one record; **flows** carry a multi-step journey.
- A flow is a **trigger + actions + logic**, built on a visual canvas.
- Every step runs server-side code for you — no scripting required.
- Reach for a flow when you can say "when X, do A, then B, then C."
- Flows are visible and logged, which makes automation accountable.
