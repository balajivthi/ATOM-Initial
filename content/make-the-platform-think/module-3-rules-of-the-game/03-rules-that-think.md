# Rules That Think

**Story so far:** Your three rules work. Now GlidePort asks for smarter automation — the kind that keeps the app maintainable as it grows: conditions, dot-walked lookups, related-record creation, and rules that know which fields changed.

## Pattern 1: Use Conditions, Not Script Checks

Prefer the **Condition** field over doing the check in the script — the rule won't even load when it doesn't match:

```
Condition: status IS delivered
```

vs. checking inside the script. Conditions keep the rule set readable and fast.

```js
(function executeRule(current, previous) {
    // only runs when status = delivered
    gs.eventQueue('glideport.order.delivered', current, current.number);
})(current, previous);
```

## Pattern 2: React Only to Real Changes with `previous`

The classic "changed" pattern — avoid firing on every update:

```js
(function executeRule(current, previous) {
    if (!previous) { return; }
    if (current.getValue('status') !== previous.getValue('status')) {
        gs.info('Status changed on ' + current.getValue('number'));
    }
})(current, previous);
```

## Pattern 3: Look Up Related Data

A Business Rule can query other tables to enrich the current record:

```js
(function executeRule(current, previous) {
    // On insert: pull the agent's city onto the order
    var agent = new GlideRecord('u_delivery_agents');
    if (current.getValue('agent') && agent.get(current.getValue('agent'))) {
        current.setValue('u_delivery_city', agent.getValue('city'));
    }
})(current, previous);
```

## Pattern 4: Create Related Records (After)

An **after** rule is the right place to spawn related work:

```js
(function executeRule(current, previous) {
    // When an order is marked urgent, create a task for the dispatcher
    if (current.getValue('urgent') === 'true') {
        var task = new GlideRecord('task');
        task.initialize();
        task.setValue('short_description', 'Handle urgent order ' + current.getValue('number'));
        task.setValue('assignment_group', 'dispatch');
        task.setValue('u_order_ref', current.getUniqueValue());   // link back via a reference field
        task.insert();
    }
})(current, previous);
```

> `current.getUniqueValue()` returns the record's sys_id — handy for reference fields back to the parent record.

## Pattern 5: Guarded Writes with `setAbortAction`

Validate as early as possible, then block with a user-friendly message:

```js
(function executeRule(current, previous) {
    if (current.getValue('weight_kg') <= 0) {
        gs.addErrorMessage('Weight must be greater than zero.');
        current.setAbortAction(true);
    }
})(current, previous);
```

## Pattern 6: Fire Events for Flows & Notifications

Events decouple Business Rules from notifications/flows. Define the event, then queue it:

```js
// in a rule script
gs.eventQueue('glideport.order.created', current, current.number, 'HIGH');
```

A **notification** (or Flow) subscribed to `glideport.order.created` handles the rest. This keeps the rule script simple and reuses your notification work from ServiceNow Basics.

## Pattern 7: Avoid Common Pitfalls

| Pitfall | Why | Fix |
| --- | --- | --- |
| Heavy work in `before` rules | Slows every save | Use `after` or `async` |
| Calling `current.update()` in `before` | Double-saves | Don't — the platform saves it |
| Infinite recursion | Rule updates the same table it runs on | Use conditions + `previous` guards, or move to async |
| Querying in a loop | Slow | Query once, cache results |
| Hardcoding sys_ids | Fragile across instances | Use `getValue()`/`getUniqueValue()` and properties |

## Lab: The Advanced Pack

1. Add a **Condition** to `Log order status change` so it only fires when `status` changes to `delivered` (or keep the script guard — discuss which is better).
2. Build a rule that looks up the agent's city and copies it onto the order on insert.
3. Build an **after** rule that creates a `task` when an order is urgent, linking back with the order's sys_id.
4. Verify all new rules appear in your update set and nothing recursed (check System Logs).

## Key Takeaways

- Use the **Condition** field to keep rules lean.
- `previous` + `current` comparison detects real changes.
- Enrich records by querying other tables; create related records in **after** rules.
- `setAbortAction(true)` + `gs.addErrorMessage()` block bad saves gracefully.
- Fire **events** instead of embedding notification logic in rules.
- Beware recursion and heavy loops; prefer `after`/`async` for expensive work.
