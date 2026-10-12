# Handle the Detours

**Story so far:** GlidePort's flows now fork, loop, and carry their data. Then a van partner's API goes down, a customer has no email on file, and a flow that looked perfect dies halfway with the order stuck in limbo. Automations need to survive the messy days too. This lesson is about failing *gracefully*.

## Flows Fail — Plan for It

A flow step can fail for very ordinary reasons:

- An external system is unreachable or returns an error.
- A required field is empty (no customer email).
- A record was deleted between the lookup and the update.
- An approval never comes.

Without handling, an error **aborts the flow** — and the order sits in limbo, often with no one the wiser.

## Try / Catch — The Safety Net

Wrap the risky steps in a **Try** block and handle failures in the **Catch**:

```
[ Try ]
   ├─ Call the van partner API
   └─ Update order → scheduled
[ Catch ]
   ├─ Log the error
   └─ Create a task for the dispatch manager
```

- **Try** holds the steps that might fail.
- **Catch** runs **only if** a step in the Try fails — perfect for alerts, fallbacks, and cleanup.

GlidePort: if booking the van fails, don't abandon the order — flag it for a human and keep the rest of the journey alive.

## Fallbacks Inside Actions

Many actions offer their own gentle failure handling. Rather than only Try/Catch at the block level, you can often:

- Provide a **default value** when a lookup returns nothing.
- Add an **If** that checks a precondition before calling the risky step:

```
If ( Customer → Email [is not empty] )
   └─ Send Notification
Else
   └─ Create Task: "Customer has no email — call them"
```

Cheap precondition checks prevent a whole class of failures.

## Logging — Leave a Trail

When something goes wrong at 2am, the **execution log** is your only witness. Make it useful:

- Use a **Log** action (or a tiny Script step: `gs.error('...')`) in the Catch branch.
- Include identifying data — `Order {{number}}` — so you can search the log.
- Distinguish **warnings** (recoverable) from **errors** (needs a human).

```
[ Catch ]
   └─ Log:  "Van booking failed for order {{number}}: {{error}}"   (level: error)
   └─ Create Task (assigned to: dispatch manager, short description: "Manual booking needed")
```

## Graceful Degradation

The goal isn't "never fail" — it's "fail without losing the work." Patterns:

| Situation | Graceful response |
| --- | --- |
| External API down | Queue a retry, or create a manual task |
| Missing required data | Alert a human; don't silently skip |
| Approval times out | Escalate to the next approver, or default to a safe choice |
| Duplicate risk | Check "already done?" before acting, or rely on run modes |

## Don't Swallow Errors Silently

A Catch that does nothing is worse than no Catch — the flow "succeeds" while the work never happened. Every Catch should do at least one of:

1. **Log** the failure with enough detail to act.
2. **Alert** someone (task, notification, chat message).
3. **Recover** — retry, fall back, or take an alternate path.

> If a Catch only logs and the failure is important, pair it with a task or notification. Logs are read by humans; tasks are *assigned* to them.

## Idempotency — Safe to Run Twice

Because flows are async and can overlap (or a scheduled job can re-fire), design steps to be **idempotent**: running them twice shouldn't double the effect.

- Check "does the task already exist?" before creating it.
- Use run modes (**Once** / **edge**) to avoid redundant runs.
- Set a value rather than incrementing it, where possible.

## Lab: Survive the Van-Partner Outage

1. In the dispatch flow, wrap the **van booking** step in a **Try**.
2. In the **Catch**, add:
   - a **Log** action at *error* level including `{{Order → Number}}`, and
   - a **Create Task** for the dispatch manager titled "Manual van booking needed".
3. Test by pointing the booking step at an invalid endpoint (or a deliberately failing record).
4. Confirm: the execution log shows the error, a task appears, and the *rest* of the flow still completes.

**Check your work:** a simulated failure no longer aborts the whole journey — it produces a logged error and a human task, and the flow finishes.

## Key Takeaways

- Flows fail for ordinary reasons; unhandled errors **abort** the run.
- **Try / Catch** is the safety net: Catch runs only on failure.
- **Precondition checks** (If) prevent a whole class of failures cheaply.
- Every Catch should **log, alert, or recover** — never swallow silently.
- Design steps to be **idempotent** so overlapping runs don't double the work.

## Best Practices

- Wrap every **external call** in a Try/Catch.
- Include **identifying data** in logs and alerts (record number, customer).
- Prefer an **assigned task** over a log line when a human must act.
- Global error handling and flow **snapshots/settings** live in Module 5 — check them before a flow goes live.
