# Your First Flow

**Story so far:** You understand *why* a flow beats a fistful of Business Rules. Time to build one. We'll automate the very first moment of a GlidePort order — the customer places it, and they should immediately hear back from us.

## The Plan

> **When an Order & Tracking record is created →** send the customer a welcome notification → set the status to `new`.

Three moves. One trigger, two actions. Let's build it.

## Step 1 — Create the Flow

1. **All → Process Automation → Flow Designer → New → Flow**.
2. **Name:** `Welcome the new order`
3. **Description:** `When an order is created, notify the customer and mark it new.`
4. Click **Submit**.

You now have an empty canvas with a single **Trigger** block waiting to be configured.

## Step 2 — Add the Trigger

1. In the **Trigger** block, choose **Record → Created**.
2. **Table:** `Order & Tracking` (your `u_order_tracking` table).
3. **Condition:** leave blank for now — we want *every* new order.
4. Toggle **Run Trigger:** *Once*. (More on run modes in Module 2.)

The trigger now hands the flow the freshly created record, and every field on it becomes available as a **data pill**.

## Step 3 — Add the First Action

1. Click the **+** just under the trigger.
2. Search the action picker for **Send Notification**.
3. Configure it:
   - **Recipient:** drag the order's *Customer* → *Email* data pill into the field.
   - **Subject:** `Your GlidePort order {{number}} is confirmed`
   - **Body:** `Thanks! We're getting order {{number}} ready for delivery. Track it any time from your account.`
4. The `{{…}}` chips are data pills — they'll be replaced with the real values at run time.

> **Tip:** hover a data pill in the picker to preview the value it will produce. If a pill is empty at run time, the notification fires with a blank — always plug a real field.

## Step 4 — Add the Second Action

1. Click the **+** under *Send Notification*.
2. Choose **Update Record** (under *Record* actions).
3. **Record:** drag the trigger's *Order & Tracking Record* pill in.
4. **Field:** `Status` → **Value:** `new`.
5. (Optional) **Field:** `Notified` → **Value:** `true`, if your table has such a column.

## Step 5 — Test the Flow

Before you turn it on, prove it:

1. Click **Test** (top-right of the designer).
2. Pick a real order record to run against, or create one on the fly.
3. Step through each action and inspect the **data pills** on the right — you'll see the actual email and number the flow is about to use.
4. Confirm the notification would go to the right person and the status update looks correct.

If a step shows red, fix the input pill it's complaining about and re-test. Testing never sends real changes until you say so.

## Step 6 — Activate

1. Click **Done** to close the test panel.
2. Flip the flow to **Active** (blue toggle, top-right).
3. Click **Save**.

Now create a brand-new Order & Tracking record and watch the flow fire:

- **Flow Designer → the flow → Executions** (or the record's *Flow Executions* related list) shows a fresh run, step by step.

## What Just Happened

You replaced a manual habit ("remember to email the customer") with a guaranteed step. Every new order now gets the same greeting, in the same order, with no human in the loop.

```
[Record Created: Order & Tracking]
        │
        ▼
[Send Notification] ──▶ customer email
        │
        ▼
[Update Record] ──────▶ status = new
```

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Notification fires with blanks | A data pill points at an empty field — pick a field that's always filled (e.g. `number`) |
| Flow never runs | The flow isn't **Active**, or the trigger table is wrong |
| Status overwritten back | Another rule/flow writes `status` later — check **Order** and run modes |
| Test "changes" don't persist | Test mode runs in a sandbox — real changes happen only once activated |

## Key Takeaways

- A flow is built in three obvious moves: **trigger → action → action**.
- **Data pills** carry real values from the trigger and earlier steps into later ones.
- Always **Test** against a real record before activating.
- **Activating** is what makes the flow run for real — and every run is logged.
