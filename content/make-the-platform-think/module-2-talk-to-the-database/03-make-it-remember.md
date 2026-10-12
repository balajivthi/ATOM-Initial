# Make It Remember

**Story so far:** Reading is great, but GlidePort needs the app to *write*: create orders when a customer requests a delivery, update the status as packages move, and retire agents who leave.

GlideRecord writes in three steps: **set values → save → check for errors**.

## Creating a Record

```js
var order = new GlideRecord('u_order_tracking');
order.initialize();                    // optional but good practice
order.setValue('number', 'ORD0011001');
order.setValue('status', 'new');
order.setValue('urgent', false);
var sysId = order.insert();            // insert() returns the new sys_id
gs.info('Created order: ' + sysId);
```

- `setValue(field, value)` sets a field.
- `insert()` saves the record and returns its **sys_id**.
- For **reference fields**, pass the related record's sys_id (or the record object).

## Updating a Record

```js
var order = new GlideRecord('u_order_tracking');
if (order.get('number', 'ORD0011001')) {
    order.setValue('status', 'shipped');
    order.update();                    // saves the change
    gs.info('Order ' + order.getValue('number') + ' is now shipped.');
}
```

### Update a whole set with `updateMultiple()`

```js
var stale = new GlideRecord('u_order_tracking');
stale.addQuery('status', 'new');
stale.setValue('status', 'cancelled');
stale.updateMultiple();                // applies to every matching record
```

## Deleting Records

```js
var agent = new GlideRecord('u_delivery_agents');
if (agent.get('name', 'Ana')) {
    agent.deleteRecord();
    gs.info('Agent record deleted.');
}
```

> **Caution:** deletions are permanent. Prefer a status like `inactive` over hard-deleting where possible.

## Checking for Errors

After `insert()` or `update()`, check the **sys_updated_by** or use the return value. A more defensive pattern:

```js
var order = new GlideRecord('u_order_tracking');
order.setValue('number', 'ORD0011002');
var sysId = order.insert();
if (!sysId) {
    gs.error('Order insert failed — check mandatory fields.');
}
```

Mandatory fields, unique constraints, or ACLs can cause writes to fail silently, so always verify.

## Dot-Walking When Writing

Set reference fields either by sys_id or by walking the related record:

```js
var order = new GlideRecord('u_order_tracking');
order.initialize();
order.setValue('number', 'ORD0011003');
order.setValue('agent', 'sys_id_of_agent');   // reference by sys_id
order.insert();
```

## The `current` Record in Business Rules

In a Business Rule (next module), the record being acted on is `current` — no query needed:

```js
current.setValue('status', 'packed');
current.update();   // only in certain rule types — see Business Rules module
```

## Lab: The GlidePort Order Cycle

1. **Create** an order with a number, status `new`, and `urgent = false`.
2. **Read** it back by number and log its status.
3. **Update** the status to `shipped` and log the change.
4. Add a `weight_kg` numeric column to Order & Tracking if missing, set it on a record, and **sum** it across the table.
5. **Delete** a test order and confirm `get()` by that number returns false.
6. Use `updateMultiple()` to set all `new` orders to `cancelled`.

## Key Takeaways

- Create: `initialize()` → `setValue()` → `insert()` (returns sys_id).
- Update: `get()` → `setValue()` → `update()`.
- Bulk: `updateMultiple()` applies to the whole result set.
- Delete: `deleteRecord()` is permanent — prefer soft statuses.
- Always check the outcome (sys_id returned, `get()` result) — writes can fail silently.
