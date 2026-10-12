# When the Platform Reacts

**Story so far:** GlidePort's team is tired of manually setting statuses and re-checking orders. They want the platform to *react*: "when an order is created, do this; when it's updated, do that." That's the job of a **Business Rule**.

## What is a Business Rule?

A **Business Rule** is a server-side script that runs automatically when a record is **inserted, updated, or deleted** on a specific table. They are the workhorses of platform automation.

```js
// Example: when an order is created, stamp it with a friendly status message
(function executeRule(current, previous /*null when async*/) {
    gs.info('New order created: ' + current.getValue('number'));
})(current, previous);
```

## Anatomy of a Business Rule

| Setting | What it controls |
| --- | --- |
| **Name** | e.g. "Set default order status" |
| **Table** | Which table it acts on (e.g. `u_order_tracking`) |
| **When to run** | Before / After, and the operation: insert, update, delete, query |
| **Order** | Sort order when multiple rules run on the same event |
| **Condition** | Optional filter — the rule only runs when it matches |
| **Script** | The server-side code to execute |

## When to Run: Before vs After

| | **Before** | **After** |
| --- | --- | --- |
| Runs | Before the record is written to the DB | After the record is written |
| `current` | Not yet saved | Saved |
| Typical use | Validate, calculate, set defaults before save | Notify, create related records, update other tables |
| Can abort | Yes (via `current.setAbortAction(true)`) | No (record already saved) |

### Before

```js
(function executeRule(current, previous) {
    if (!current.getValue('status')) {
        current.setValue('status', 'new');   // default before save
    }
})(current, previous);
```

### After

```js
(function executeRule(current, previous) {
    // Order saved — tell the warehouse via an event
    gs.eventQueue('glideport.order.created', current, current.number);
})(current, previous);
```

## The `current` and `previous` Variables

- **`current`** — the record being acted on. Read/write fields; `update()` persists changes (in "after" rules).
- **`previous`** — a snapshot of the record **before** this operation (null on insert and in async rules). Perfect for "did field X change?" logic.

```js
(function executeRule(current, previous) {
    if (previous && current.getValue('status') !== previous.getValue('status')) {
        gs.info('Order status changed from ' + previous.getValue('status') +
                ' to ' + current.getValue('status'));
    }
})(current, previous);
```

## Rule Types

| Type | Runs |
| --- | --- |
| **Display** | When a record is opened (no `current` writes) |
| **Before insert/update/delete/query** | As the operation happens |
| **After insert/update/delete/query** | After the operation |
| **Async** | After the operation, queued in the background |

## A Simple Real-World Example

Create a Business Rule on `u_order_tracking`:

1. **Name:** `Set order to new on insert`
2. **Table:** Order & Tracking
3. **When to run:** Before, Insert
4. **Script:**
   ```js
   (function executeRule(current, previous) {
       if (!current.getValue('status')) {
           current.setValue('status', 'new');
       }
       current.setValue('urgency', 'standard');   // assume your table has this column
   })(current, previous);
   ```
5. **Order:** 100 (lower runs first)

Now every new order auto-gets a default status.

## Best Practices

- Keep rules **small and focused** — one job per rule.
- Use **Order** to control execution sequencing.
- Use **Condition** to skip work when it's not needed.
- Use `previous` to detect field changes instead of comparing in memory.
- Only put heavy work in **after/async** rules; keep `before` rules fast.

## Key Takeaways

- Business Rules react to record insert/update/delete on a table.
- **Before** = validate/default before save; **After** = notify/create related things.
- `current` is the record, `previous` is its old state (null on insert).
- Rules are server-side, so they always run and are trustworthy.
- Name rules clearly and set their Order explicitly.
