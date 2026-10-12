# Run It Your Way

**Story so far:** The flow starts at the right moment and only for the right changes. There's one more dial on the trigger: **how often** it runs — once per record, on every update, or on a schedule. Get this wrong and you'll either spam the customer or miss an update entirely.

## The Run Mode Dial

Record triggers expose a **Run Trigger** setting. The common modes:

| Run Trigger | Means |
| --- | --- |
| **Once** | Run one time per matching record; later updates don't re-fire |
| **For each update** (default) | Run every time the trigger condition is met |
| **Only if condition was false and becomes true** | "Edge" firing — run when a condition flips from false to true |
| **For each unique change** | Run per changed field / group of fields |

The default is usually fine, but the *edge* and *unique change* modes prevent a mountain of accidental re-runs.

## Why "For Each Update" Can Bite

Consider: "When an order is priority, escalate it."

If the run mode is *for each update*, the flow re-escalates the order on **every** save — the agent's note, the address fix, anything. You get duplicate tasks, duplicate emails, and a confused team.

Fix: switch to **Once**, so the escalation happens a single time, or use **Only if condition was false and becomes true**, so it fires exactly when the order *becomes* priority.

## Once vs Edge — Picking Between Them

| Mode | Best when |
| --- | --- |
| **Once** | The work should happen at most once, ever, per record (create the van task) |
| **Only if … false → true** | The work should happen each time a condition flips on (each time it becomes priority) |
| **For each update** | The work must re-run on every change (recalculate the delivery ETA on every field edit) |
| **For each unique change** | React differently per changed field |

> **Rule of thumb:** if you're about to guard a flow with an `If (task already exists)` inside, first ask whether the trigger's run mode could have prevented the duplicate for free.

## Scheduled Flows: From and To

A scheduled trigger has its own time dials:

- **Repeat:** free text like `Every day at 17:00`, `Weekly on Monday`, or a cron-style expression.
- **Starting:** when the schedule begins.
- **Run as:** the user the flow executes as (the *run-as* user matters for permissions!).

For a nightly job, the flow has **no record**, so it can't be "once per record." Each scheduled tick is simply one run — design the flow to *find* its work (Look Up Records → For Each) and be safe if it runs twice.

## Who Runs the Flow? (Run As)

Every flow runs **as a user**, and that user's permissions apply to every record read and write. Two choices:

| Runs as | Effect |
| --- | --- |
| **System / a service account** | Effectively full access; the flow can always do its job, regardless of who triggered it |
| **The triggering user** | The flow is limited to what *that* user can see and change |

GlidePort: a "flag a risky order" flow should run as **system** (an agent shouldn't be blocked from triggering it just because *they* can't edit the risk table). A "show *my* orders" flow, by contrast, must respect the user.

> **Caution:** "runs as system" bypasses field-level security for the flow's actions. Use it for genuine back-office work, not to hide a permissions issue.

## Async Means "In the Background"

Flows run **asynchronously** — the user's save completes immediately; the flow proceeds behind the scenes. That's usually what you want (no waiting), but it means:

- The flow sees the record **after** the save.
- If the user re-saves quickly, several runs can overlap (**Once**/**Edge** modes help).
- Order-sensitive work should be guarded rather than assumed.

## Lab: Fix the Escalation Trigger

The "escalate priority orders" flow currently creates a task on every save.

1. Set the trigger to **Record → Created or Updated**, condition `Priority is Priority`.
2. Change **Run Trigger** to **Only if condition was false and becomes true**.
3. Test: flip an order to priority → one task. Save it again → no new task.
4. Now switch to **Once** and repeat → also one task, but also confirmed for later flips.

**Check your work:** you can describe, in one sentence, which mode stops the duplicates — and *why* it's the cheapest fix.

## Key Takeaways

- The trigger's **Run Trigger** mode controls how often a record flow fires: **Once**, **for each update**, **edge (false→true)**, or **per unique change**.
- Prefer fixing duplicates at the trigger before adding guards inside the flow.
- Scheduled triggers bring their own **schedule** and **run-as** settings; each tick is a fresh run.
- **Run as** determines the permissions the flow operates with — choose system for back-office, user for personal work.
- Flows are **asynchronous**: they run after the save, in the background.

## Best Practices

- Default to **Once** or **edge** firing for "do it once" work; reserve *for each update* for recalculations.
- Name your run-as service account clearly and give it *just enough* access.
- Make scheduled flows **idempotent** — safe to run twice.
- If you see duplicates, suspect the run mode before you suspect the logic.
