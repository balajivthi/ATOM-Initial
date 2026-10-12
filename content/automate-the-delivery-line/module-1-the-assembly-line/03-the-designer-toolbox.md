# The Designer Toolbox

**Story so far:** You built a working flow and watched it log a real run. Now let's open the toolbox properly — the trigger, the actions, the logic blocks, the data, and the little controls that keep a big flow readable.

## The Canvas at a Glance

```
┌───────────────────────────────────────────────┐
│  Trigger                                      │
│  ┌─────────────────────────────┐              │
│  │ Record Created · Order      │              │
│  └─────────────────────────────┘              │
├───────────────────────────────────────────────┤
│  Actions & Flow Logic                         │
│  ┌─────────────────────────────┐              │
│  │ Send Notification           │  ← Action    │
│  └─────────────────────────────┘              │
│  ┌─────────────────────────────┐              │
│  │ If / For Each / Wait / ...  │  ← Logic     │
│  └─────────────────────────────┘              │
└───────────────────────────────────────────────┘
```

Everything you'll ever build is one of five kinds of block: **Trigger**, **Action**, **Flow Logic**, **Subflow**, or **Flow Variable**.

## Triggers — What Starts the Flow

The trigger is the *only* block that can be first. Pick the event and the data source:

| Trigger | Fires when |
| --- | --- |
| **Record → Created / Updated / Deleted** | A row changes on a table you choose |
| **Scheduled** | On a schedule you define (daily, weekly, `Run once`, or a cron-ish repeat) |
| **Inbound Email** | A message arrives in a mailbox you set up |
| **REST** / **Webhook** | An external system calls in |
| **Service Catalog** | A catalog item is ordered |
| **SLA** | A task's service-level timer changes state |

We'll tour the record triggers in Module 2.

## Actions — One Unit of Work

Actions are the **doers**. A few of the most-used ones:

| Action category | Examples |
| --- | --- |
| **Record** | Create Record, Update Record, Delete Record, Look Up Record(s) |
| **Notification** | Send Notification, Send Email |
| **Approval** | Ask for Approval |
| **Task** | Create Task, Create Catalog Task |
| **Communication** | Send SMS, Post a message to a channel |
| **Flow** | Call a Subflow, Wait for a Subflow |
| **Automation** | **Script** (drop into JavaScript when no action exists), REST step |

If the action you want doesn't exist yet, you'll learn to **build a custom action** in Module 4 — that turns any repeatable job into a drag-and-drop block.

## Flow Logic — Steering the Route

Logic blocks don't do work themselves; they decide *which* steps run:

| Block | What it does |
| --- | --- |
| **If** | Branch down one path when a condition is true |
| **For Each** | Loop over every item in a list (all overdue orders, all line items) |
| **Wait for condition** | Pause the flow until something becomes true, with a timeout |
| **Do until** | Repeat a block until a condition is met |
| **Parallel** | Run two paths at the same time and re-join |
| **Try / Catch** | Handle failures gracefully instead of aborting (Module 3) |

## Data Pills — Piping Values

A **data pill** is a chip that represents a value. Drag one from the **Data** panel on the right into any input field:

- From the **trigger**: `Order & Tracking Record → Number`, `→ Customer → Email`.
- From an **earlier action**: `Create Task → Task Record → Sys ID`.
- From a **flow variable**: a value you computed and named.

Pills free you from hardcoding. `Please deliver {{order.number}}` always uses the *current* order.

## Stages — Chapters for Long Flows

A **stage** is a labelled band on the canvas. Wrap steps in stages and a 30-step flow reads like a story:

```
Stage: Intake        →  verify the order, assign the agent
Stage: Fulfilment    →  book the van, await approval
Stage: Wrap-up       →  notify the customer, close the task
```

Stages show up in the execution log too, so a stalled run points you straight at the chapter that failed.

## Flow Variables — Named Storage

Need to hold a value mid-flow — a computed total, a status message, a flag? Add a **flow variable** (e.g. `var_van_booking_id`), set it in one action, and read it as a pill in a later one. Variables keep long flows from repeating expensive lookups.

## The Controls That Save You

| Control | Why it matters |
| --- | --- |
| **Test / Run** | Dry-run against a real record and step through each action |
| **Executions** | The run history — click a run to replay every step |
| **Active toggle** | Off = saved but dormant; On = live for everyone |
| **Save vs Done** | Save keeps edits; Done closes the canvas |
| **Templates & copy** | Duplicate a flow as a starting point for the next one |

## Lab: Tidy the Welcome Flow

Open the flow you built in the previous lesson and make it production-grade:

1. Add a **Stage** called `Intake` around the notification and update steps.
2. Add a **flow variable** `var_notified_at` and set it to the current date/time (use the **Script** action: `return new GlideDateTime().getDisplayValue();`).
3. Put that value into the notification body: `Confirmed at {{var_notified_at}}`.
4. Re-test and check the **Executions** log shows the stage and the variable.

**Check your work:** the flow reads as a labelled story, and the run log shows the computed timestamp.

## Key Takeaways

- Five block types: **Trigger, Action, Flow Logic, Subflow, Flow Variable**.
- Triggers start; actions do; logic decides.
- **Data pills** pipe real values from trigger and earlier steps.
- **Stages** make long flows readable and debuggable.
- Always run through **Test** and keep an eye on **Executions**.
