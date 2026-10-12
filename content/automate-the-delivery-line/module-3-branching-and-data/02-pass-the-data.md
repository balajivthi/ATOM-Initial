# Pass the Data

**Story so far:** The dispatch flow forks and loops correctly — but a fork is useless if the express task goes out with a blank address. Now we make sure the *right values* travel from step to step: data pills, flow variables, and a script escape hatch when no action exists.

## Values Flow Downhill

Think of the canvas as a river. Values are created near the top (by the trigger) and can be carried into anything **below** them. A step can use:

- **Trigger data** — the record and its fields.
- **Earlier action output** — e.g. the Sys ID of a task you just created.
- **Flow variables** — named values you set along the way.

Later steps **cannot** reach *up* to values created below them — so order matters. If a step needs a value, create that value above it.

## Data Pills, Revisited

A **data pill** is the drag-and-drop representation of a value. Dot-walking gets you deep fields:

| Pill | Resolves to |
| --- | --- |
| `Order & Tracking Record → Number` | `ORD0010001` |
| `Order & Tracking Record → Customer → Email` | the customer's email |
| `Order & Tracking Record → Customer → Manager → Name` | an attribute two hops away |

Dot-walking works as long as there's a **reference** field to follow. If a hop is empty at run time, the pill comes back blank — guard it.

## Flow Variables — Named Storage

Sometimes you must **compute** a value and reuse it later, or across branches. That's a **flow variable**:

1. Add a flow variable, e.g. `var_eta`.
2. Set it in an action (a **Set Flow Variables** block, or as an output of another action).
3. Read it as a pill downstream: `var_eta`.

Good uses:

- A computed **delivery window** used by three later notifications.
- A **flag** ("needs manager approval") set in one branch, checked in another.
- An **external reference** returned by a REST call, needed again at wrap-up.

Using a variable once is fine; using it in several places is where it earns its keep.

## Action Outputs — Values With a Home

Every action that does something meaningful returns data. When you add an action, its result appears as a pill you can wire into the next step:

```
[ Create Task ] ──▶ outputs:  Task Record
                                     └▶ Sys ID
                                     └▶ Assigned To
                                     └▶ Number
```

GlidePort: create the van task, then **send its number** to the driver in the very next step.

## The Script Step — When No Action Exists

The action library is huge, but not infinite. When there's no ready-made action, drop in a **Script** action and write a little JavaScript. It can take pills as **inputs** and expose a **value** as output:

```js
// Inputs: order (a record pill)
// Output: var_delivery_window

(function execute(inputs, outputs) {
    var order = inputs.order;
    var priority = order.getValue('u_priority');

    outputs.delivery_window = (priority === 'priority') ? 'Today, before 12:00'
                                                        : 'Within 3 working days';
})(inputs, outputs);
```

Then use `var_delivery_window` (or the action's output pill) later. The Script step is the bridge between the visual flow and the full server-side API — GlideRecord, GlideDateTime, everything.

> **Design rule:** reach for a Script step only when you've checked the action library. If you find yourself scripting the same thing twice, that's your cue to build a **custom action** (next module) so it becomes a reusable block.

## Passing Data Correctly: A Checklist

| Question | Why it matters |
| --- | --- |
| Does this step need data from **earlier**? | If yes, the pill must be created above it |
| Is the source field **reliably populated**? | Empty pills → blank emails, failed writes |
| Am I **dot-walking** a reference that may be null? | Wrap it in an If, or default it |
| Will I need this value **again later**? | Store it in a **flow variable** |
| Is this logic **repeated** elsewhere? | Extract it to a custom action/subflow |

## Lab: Carry the ETA All the Way

1. In the dispatch flow, add a **Script** action right after the trigger that computes `var_delivery_window` from the order's priority (use the snippet above).
2. Use that pill in the **customer notification** body: `Expected: {{var_delivery_window}}`.
3. In the courier task's description, include both `{{Order → Number}}` and the same window.
4. Test with a priority order and a standard order; confirm the text differs correctly.

**Check your work:** one computed value, used in two different steps, branching correctly by priority — with no duplicated logic.

## Key Takeaways

- Values flow **downhill**: trigger → action → action; order matters.
- **Data pills** carry values; **dot-walking** reaches referenced records.
- **Flow variables** store named values for reuse across branches.
- **Action outputs** (like a created task's Sys ID) are pills too.
- The **Script** action is the escape hatch — but repeated logic belongs in a **custom action**.

## Best Practices

- Compute a value **once**, store it in a variable, reuse it — don't recompute in every branch.
- Never assume a reference pill is populated; guard with an If or a default.
- Keep Script steps small and side-effect free where you can.
- Name flow variables clearly (`var_eta`, not `var1`).
