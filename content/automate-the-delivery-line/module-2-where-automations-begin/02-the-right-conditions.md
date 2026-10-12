# The Right Conditions

**Story so far:** Your flows start at the right *moments*. But a trigger on "order updated" fires for **every** update — a typo fix, a note, a status change. GlidePort's agents don't want a fresh email when someone corrects a spelling. This lesson is about teaching a flow to ask *"is this update the one I care about?"*

## Why Conditions Matter

Without a condition, an *updated* trigger fires on every save. That means:

- Customers get spammed by irrelevant changes.
- Work runs that doesn't need to.
- Ordering gets confusing because several flows all react.

A **trigger condition** is a filter: the flow runs only when the filter is true.

## Adding a Trigger Condition

In the trigger block:

1. Click **Add condition**.
2. Build a comparison from data pills and literals:

```
  Order & Tracking Record → Status   [changes]
```

or

```
  Order & Tracking Record → Priority   [is]   Priority
```

Conditions support the usual operators: **is, is not, is empty, is not empty, changes, contains, greater than**, and so on.

## Watch the Right Field

A classic trap: "email when the status changes," written as *Updated on any field*. A user fixes a typo, and off goes another email. Instead:

- Use the **updated** trigger with a **field watch** on `Status`.
- Then add an **If** in the flow only if you need extra logic.

```
Trigger: Record → Updated · Order & Tracking
Condition: Status [changes]

Flow:
  If ( Status is "shipped" ) → Send Notification (tracking link)
```

The **"changes"** operator is the key — it's true only on the update where that field's value actually moved.

## Conditions vs If Blocks

Both ask a question; they live in different places:

| | **Trigger condition** | **If block** |
| --- | --- | --- |
| Where | On the trigger | Inside the flow |
| Effect | Flow never starts if false | Flow starts, but a branch is skipped |
| Cost | Cheapest — filters runs at the source | Flow engine starts, then decides |
| Use for | "Only react to *this* kind of change" | "Given we started, choose path A or B" |

**Guideline:** put the *cheap "should I even bother?"* test on the trigger; put *branching logic* in If blocks.

## Conditions on Scheduled Flows

A scheduled trigger has no `current` record, so there's nothing to filter at the trigger. Instead you filter in the flow:

1. Trigger: **Scheduled**.
2. **Look Up Records** action with an encoded query: `status=shipped^u_delivery_date<javascript:gs.now()`.

That query is your "condition" — it selects only the overdue orders to loop over.

## Building a Real Filter

GlidePort's **"order is at risk"** flow should run when an order is **priority** *and* not yet delivered:

```
Trigger: Record → Created or Updated · Order & Tracking
Conditions:
  Priority  [is]        Priority
  Status    [is not]    Delivered
```

If either fails, the flow doesn't run — saving the engine work and the customer from noise.

> **Tip:** conditions AND together by default. Use **OR** groups only when you truly mean "any of these."

## A Shortcut: Run Once Per Record

Some record triggers expose **Run Trigger: Once** — the flow runs once for a record and then won't re-fire for that same record, even on later updates. It's handy when multiple updates in quick succession would otherwise produce duplicate work (for example, "create the van task the first time the order is scheduled").

Set it on the trigger alongside your conditions.

## Lab: Stop the Spam

The finance team complains that the order-status email fires too often.

1. Take the **status email** flow.
2. On the trigger, change it to **Record → Updated** with a field watch on `Status`.
3. Add a second condition: `Status [is not empty]`.
4. Test: update a *different* field (e.g. a note) — confirm no execution appears.
5. Then set `Status` to `shipped` — confirm the flow fires once.

**Check your work:** editing an unrelated field produces **no** execution; changing `Status` produces exactly one.

## Key Takeaways

- A **trigger condition** filters runs at the source — the cheapest place to say "not this one."
- **"changes"** fires only when the watched field actually moves; it's the antidote to update-spam.
- Use **trigger conditions** for "should I run at all," and **If blocks** for in-flow branching.
- Scheduled flows have no `current` record — filter with a **Look Up Records** query instead.
- **Run Once** guards against duplicate runs for the same record.

## Best Practices

- Always ask: *what fields must actually change* for this flow to be worth running?
- Keep trigger conditions short — 2–3 clauses; push deeper logic into the flow.
- Encode negative cases explicitly (`Status is not Delivered`) to avoid surprises.
- Test by changing an *irrelevant* field and confirming silence.
