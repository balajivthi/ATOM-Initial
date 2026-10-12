# When to Use What

**Story so far:** You can now build flows, subflows, and custom actions. But the platform also has Business Rules, Scheduled Jobs, Workflows, and Client Scripts — and a good engineer picks the *right* tool, not just the favourite one. This lesson is the decision guide.

## The Automation Toolbox

| Tool | Runs | Best for |
| --- | --- | --- |
| **Business Rule** | Server-side, on a record event | A quick reflex: default a field, validate, block a save |
| **Flow** | Async flow engine | Multi-step journeys, approvals, waits, cross-table work |
| **Scheduled Job** | On a clock | Simple recurring script (cleanup, sync) |
| **Scheduled Flow** | On a clock | Recurring work that benefits from actions/logging |
| **Client Script** | Browser | Instant form feedback, before the user saves |
| **UI Policy / UI Action** | Browser | Show/hide fields, add buttons |
| **Workflow** | Server-side (legacy) | Existing legacy workflows only — prefer flows for new work |

## The Decision Tree

Ask, in order:

```
Does it need to happen instantly in the browser,
before the user saves?            → Client Script / UI Policy

Is it a one-line reflex on a single record event? → Business Rule

Is it multi-step, or spans time/tables/approvals? → Flow

Is it purely "every day at X, do Y"?   → Scheduled Job (script) or Scheduled Flow

Is it legacy and already a Workflow?   → leave it, migrate when touched
```

## Flow vs Business Rule — The Classic Call

They overlap, so draw the line deliberately:

| Prefer a **Business Rule** when… | Prefer a **Flow** when… |
| --- | --- |
| It's one action on insert/update | It's three or more steps |
| It must run **before** the save (validate, abort, set a field synchronously) | Order/isolation doesn't need to be synchronous |
| It's a developer's one-liner | A non-developer should read and maintain it |
| Performance-critical, minimal overhead | Approval, wait, timeout, or cross-table work |

> **Key distinction:** a **before** Business Rule can *change or block* the save as it happens. Flows are **after-the-fact** and asynchronous. If you need to stop a save, that's a Business Rule (or a client-side check), not a flow.

## Scheduled Job vs Scheduled Flow

| | **Scheduled Job** | **Scheduled Flow** |
| --- | --- | --- |
| Built with | A JavaScript script | Visual actions |
| Best for | A short, self-contained script | Multi-step recurring work with logging |
| Visibility | Code only | Steps + executions |
| When in doubt | — | Prefer a flow for maintainability |

## Don't Duplicate the Reflex

A common smell: a Business Rule sets a default, *and* a flow reacts to the same event and does overlapping work. Pick one owner per event. If both must exist, make the responsibilities disjoint and document them.

## Mixing Tools Well

The tools are strongest together:

- **Client Script** validates the form for instant feedback → **Business Rule** enforces the same rule server-side (never trust the browser alone).
- **Business Rule** sets a default on insert → **Flow** takes over the multi-day journey.
- **Flow** calls a **custom action** that wraps a **Script Include** shared with other code.

GlidePort's layering:

```
Browser:   Client Script   → "is the postcode filled?"  (instant)
Server:    Business Rule   → enforce the rule, set defaults
Journey:   Flow            → van booking, approvals, waits, notifications
Clock:     Scheduled Flow  → nightly overdue chase
Reuse:     Script Include  → shared logic called by all of the above
```

## A Quick Reference

| I need to… | Use |
| --- | --- |
| Default `status` before insert | Business Rule (before) |
| Block a save with a validation message | Business Rule (before) + error message |
| Toggle a field's visibility as the user types | UI Policy / Client Script |
| Send an email the moment a record changes | Flow (record trigger) |
| Get manager approval, then continue | Flow (Ask for Approval + wait) |
| Recalculate a score nightly | Scheduled Flow (or Scheduled Job) |
| Expose logic to several tools | Script Include |
| Wrap an external API as a step | Custom Action |

## Lab: Assign the Right Tool

For each GlidePort need, choose the tool and say why:

1. Prevent an order being saved without a customer.
2. Chase all overdue orders at 17:00 daily.
3. Email a tracking link when `status` becomes `shipped`.
4. Show a red hint under a field the moment the user types an invalid postcode.
5. Get a manager's approval before an order over a limit proceeds.

**Check your work:**
1. Business Rule (before) — must block the save. · 2. Scheduled Flow. · 3. Flow (record updated, field-watch). · 4. Client Script / UI Policy. · 5. Flow (approval).

## Key Takeaways

- Match the tool to the **timing**: browser-now, server-reflex, journey, or clock.
- **Business Rules** win for synchronous one-line reflexes (especially **before** save).
- **Flows** win for multi-step, cross-table, timed, and approval work.
- Prefer a **flow** over a Scheduled Job for anything non-trivial and maintainable.
- Layer tools deliberately, and avoid overlapping owners for the same event.

## Best Practices

- One **owner** per event; if two tools must touch it, split the responsibilities.
- Enforce validation **server-side** even if the client already checked it.
- Migrate legacy **Workflows** to flows when you next touch them.
- Document *why* a piece of automation lives where it does — future-you will ask.
