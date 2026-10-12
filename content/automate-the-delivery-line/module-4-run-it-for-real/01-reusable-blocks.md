# Reusable Blocks

**Story so far:** GlidePort now has several flows, and they keep repeating the same moves — "book a van," "notify the customer," "flag for a manager." Copy-paste is how automation rots: fix a bug in one copy and forget the other four. This lesson packages repeated work into blocks you build once and call anywhere.

## Two Kinds of Reusable Block

| | **Subflow** | **Custom Action** |
| --- | --- | --- |
| Contains | A whole sequence of triggers-free steps | One atomic job, with defined inputs/outputs |
| Called from | Another flow (and can be called on demand) | Any flow, as a normal action |
| Inputs/outputs | Yes — you define them | Yes — you define them |
| Best for | A multi-step routine (a "mini-flow") | A single reusable operation (wrap a script/API) |
| Appears in the action picker | Under **Flow → Action** | Under **Custom Actions** |

Both live in `sys_hub_sub_flow` / `sys_hub_action_type_definition`. The difference is **granularity**: a subflow is a routine, a custom action is a step.

## Subflows — Write a Routine Once

A **subflow** is a flow with no trigger of its own. You define **inputs** (what it needs) and **outputs** (what it returns), then call it from any flow.

GlidePort's **"Book a delivery van"** routine:

```
Subflow: Book Delivery Van
  Inputs:  order (record), requested_date (date)
  Steps:   check availability → reserve van → create task → return booking id
  Outputs: booking_id, van_number
```

Now *any* flow that needs a van calls one block:

```
[ Call Subflow: Book Delivery Van ]
   inputs:  order = {{Order}}, requested_date = {{var_requested}}
   outputs: booking_id = {{var_van_booking_id}}
```

One definition, many callers, one place to fix.

### When to extract a subflow

- The same sequence appears in **two or more** flows.
- A branch on one canvas has grown past a screenful.
- You want a **named step** that reads clearly in another flow ("Book Delivery Van" beats ten anonymous actions).

## Custom Actions — Wrap a Script or an API

A **custom action** turns a specific job into a **drag-and-drop step** with typed inputs and outputs. Two common flavours:

1. **Script action** — wrap server-side JavaScript.
2. **REST action** — wrap an external API call (with the request built for you).

Build one:

1. **Flow Designer → New → Action**.
2. Add **inputs** (e.g. `order_number`).
3. Add **steps** (a REST call, or a script step).
4. Define **outputs** (e.g. `eta`).
5. Publish — it now shows in the action picker for every flow.

GlidePort's **"Get van ETA"** custom action wraps the partner API:

```
Action: Get Van ETA
  Input:  van_number (string)
  Step:   REST → GET https://dummyjson.com/carts/{van_number}
  Output: eta (string)
```

Any flow can now ask for a van's ETA without knowing the API details.

### Action vs subflow — how to choose

| Ask yourself | Reach for |
| --- | --- |
| "Is this a **single** operation I want as one step?" | **Custom action** |
| "Is this a **routine** of several steps?" | **Subflow** |
| "Will it call an **external system**?" | **Custom action** (REST) — often wrapped in a subflow |
| "Will it be invoked by **many** flows?" | Either — both are callable everywhere |

## The Payoff: A Block Library

Over time GlidePort accumulates a small library of building blocks:

```
Custom Actions            Subflows
──────────────            ────────
Get Van ETA               Book Delivery Van
Notify Customer           Assign Nearest Agent
Flag For Manager          Close Out Order
```

New flows are now assembled almost entirely from named blocks — faster to build, easier to read, and consistent across the business.

> **Governance tip:** prefix custom blocks with a domain name (`GlidePort - Get Van ETA`) and document their inputs/outputs so teammates can trust them.

## Lab: Extract the Van Booking

1. Take the dispatch flow's van-booking steps and move them into a new **subflow** `Book Delivery Van` with inputs `order` and `requested_date`, and output `booking_id`.
2. Replace the original steps with a **Call Subflow** block.
3. Build a **custom action** `Get Van ETA` (a REST wrapper is fine to stub).
4. Use the subflow's `booking_id` to call `Get Van ETA` in the dispatch flow.
5. Confirm the dispatch flow reads as a short list of named blocks.

**Check your work:** the dispatch canvas is now a handful of readable blocks; the van logic exists in exactly one place.

## Key Takeaways

- **Subflows** are triggerless routines with inputs/outputs — call them from any flow.
- **Custom actions** turn one job (script or REST) into a reusable, typed step.
- Extract when logic **repeats**, a branch grows long, or a named step improves readability.
- A growing **block library** lets new flows be assembled, not coded.
- Document and prefix shared blocks so the team can reuse them safely.

## Best Practices

- Extract on the **second** copy — not never, not always on the first.
- Keep custom actions **single-purpose** and give them clear input/output names.
- Wrap external calls in a custom action so the Try/Catch and retries live in one place.
- Version and document shared blocks; a silent change to a popular subflow affects every caller.
