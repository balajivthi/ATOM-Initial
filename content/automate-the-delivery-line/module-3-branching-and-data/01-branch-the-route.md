# Branch the Route

**Story so far:** Your flows start at the right time and only when they should. So far they run in a straight line — top to bottom. Real deliveries turn corners: priority orders jump the queue, bulky items need a special van, some orders need a manager's okay. A flow steers with **flow logic**.

## Straight Lines Only Go So Far

A linear flow is `A → B → C`. The moment reality forks, you need **If**:

```
                   ┌── true ──▶ [ Assign express courier ]
[ If priority? ] ──┤
                   └── false ─▶ [ Assign standard agent ]
```

The **If** block evaluates a condition and sends the flow down one path. Each path can hold its own actions, its own branches, and its own If blocks — branching nest as deep as the problem needs.

## If — Take the Fork

Add an **If** and build a condition from data pills:

```
If   Order & Tracking Record → Priority   [is]   Priority
```

then drop actions on the **true** and **false** branches. When both paths re-join, the flow continues as one line again.

> **Tip:** the **false** branch is optional. Omit it and the flow simply skips the true-branch work when the condition fails.

## For Each — Loop Over a List

Some work repeats over a set of records — *all* overdue orders, *every* line item in an order. A **For Each** block takes a **list** and runs its inner steps once per item:

```
[ Look Up Records: overdue orders ] ─▶ [ For Each order ]
                                          └▶ [ Send reminder ]
                                          └▶ [ Update order → chased ]
```

Inside the loop, the current item is a data pill (`For Each → item`). Everything downstream can use it.

**Watch out for:** looping over an *empty* list. A For Each over zero items simply does nothing — safe, but silent. If "no orders" is itself important, add an If after the lookup.

## Wait — Pause for a Condition

Deliveries take time. A flow can **Wait for condition** — pause until something becomes true, *or* a timeout elapses:

```
[ Order shipped ] ─▶ [ Wait for condition: status = delivered ]
                              │ (up to 3 days)
                              ├── met ──▶ [ Email "Delivered!" ]
                              └── timed out ─▶ [ Email "Where is it?" ]
```

This is the block that lets a "journey" span days without a human watching. Always set a timeout so a stalled wait doesn't hang forever.

## Do Until — Repeat Until Done

**Do until** runs a block again and again until a condition is met — useful for polling an external system until it reports ready:

```
[ Do until: van status = confirmed ]
   └▶ [ Check van partner API ]
   └▶ [ Wait 5 minutes ]
```

Cap the retries (or the wait) so a stuck external service can't loop forever.

## Parallel — Two Roads at Once

When two steps don't depend on each other, run them **in parallel** to finish sooner:

```
              ┌──▶ [ Email the customer ]
[ Order placed ] ─┤
              └──▶ [ Notify the warehouse ]
```

The flow waits for both paths to finish, then continues. Use it for genuinely independent work; skip it when one step needs the other's output.

## Nesting and Readability

Logic blocks nest — a **For Each** containing an **If**, inside an **If**. That power is easy to abuse:

- **Extract to a subflow** when a branch grows past a screenful (Module 4).
- **Name your actions** meaningfully so the canvas reads like sentences.
- **Use stages** to group branch-heavy flows into chapters.

## Putting It Together

GlidePort's "smart dispatch" flow:

```
Trigger: Record → Created · Order & Tracking
  │
  ├─ If ( Priority is Priority )
  │     └─▶ Assign express courier
  ├─ Else
  │     └─▶ Look Up Records (available agents)
  │           └─▶ For Each agent
  │                 └─▶ If ( agent covers the postcode ) → Assign this agent; stop looping
  └─▶ Wait for condition ( order delivered, timeout 3 days )
        ├─ met       → Email the customer a thank-you
        └─ timed out → Escalate to dispatch manager
```

One trigger, a fork, a loop, a pause, and a timeout — a whole business process on one canvas.

## Lab: Fork the Dispatch

Extend the welcome flow into a branching dispatch flow:

1. After the trigger, add an **If**: `Priority is Priority`.
2. **True:** create a task for the express courier.
3. **False:** look up available standard agents and **For Each** over them, assigning the first that matches the postcode.
4. Add a **Wait for condition** (`delivered`, timeout 3 days) with an escalation on timeout.
5. Test both a priority and a standard order; confirm each path behaves.

**Check your work:** a priority order takes the express branch; a standard order loops the agents; both reach the wait.

## Key Takeaways

- **If** forks the route on a condition; the false branch is optional.
- **For Each** loops over lists — and silently does nothing on an empty list.
- **Wait for condition** pauses for days, with a timeout path.
- **Do until** repeats a block; **Parallel** runs independent paths at once.
- Branch-heavy flows stay readable with **named actions**, **stages**, and **subflows**.

## Best Practices

- Prefer a **Look Up Records + For Each** over repeating near-identical steps by hand.
- Always set a **timeout** on Wait and a **cap** on Do until.
- Use **Parallel** only for steps with no dependency between them.
- When a branch outgrows a screenful, extract it into a **subflow**.
