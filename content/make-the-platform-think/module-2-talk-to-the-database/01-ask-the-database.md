# Ask the Database

**Story so far:** GlidePort's delivery app has data — agents, orders, statuses. Your first real task as a developer: read that data from scripts. The tool is **GlideRecord**, the gateway to the platform's database.

## What is GlideRecord?

**GlideRecord** is the server-side API for querying and working with table records. Think of it as a *typed cursor* over a table:

```js
var agent = new GlideRecord('u_delivery_agents');
agent.get('name', 'Ana');

gs.info(agent.getValue('name') + ' — ' + agent.getValue('phone'));
```

You create it with a **table name**, then navigate its records like an object.

## The Three Ways to Find a Record

### 1. `get()` — fetch by value

```js
var order = new GlideRecord('u_order_tracking');
var found = order.get('number', 'ORD0010001');
if (found) {
    gs.info('Order found: ' + order.getValue('number'));
} else {
    gs.info('Order not found.');
}
```

`get()` loads **exactly one** record and moves the cursor to it. It returns `true`/`false`.

### 2. `get()` — fetch by sys_id

```js
var order = new GlideRecord('u_order_tracking');
if (order.get('a1b2c3d4e5f6...')) {   // pass the sys_id directly
    gs.info('Loaded order ' + order.number);
}
```

### 3. `query()` — iterate over many records

```js
var agents = new GlideRecord('u_delivery_agents');
agents.query();

while (agents.next()) {
    gs.info(agents.getValue('name') + ' | ' + agents.getValue('status'));
}
```

- `query()` runs the query but does **not** load anything yet.
- `next()` advances the cursor to the next matching record; each call returns `true` until the end.

## Reading Field Values

Use **`getValue()`** — it returns the value as a string:

```js
var order = new GlideRecord('u_order_tracking');
if (order.get('number', 'ORD0010001')) {
    var number = order.getValue('number');
    var status = order.getValue('status');
    var urgent  = order.getValue('urgent');      // boolean comes back as 'true'/'false'
    gs.info(number + ' is ' + status);
}
```

> Use `getValue()` (string) for display and logic. `getDisplayValue()` returns the *display value* of a reference field (e.g. a name instead of a sys_id).

## Dot-Walking Related Records

A **reference field** points at another table. You can walk into it with dots:

```js
var order = new GlideRecord('u_order_tracking');
if (order.get('number', 'ORD0010001')) {
    // 'agent' is a reference to u_delivery_agents
    gs.info('Assigned agent: ' + order.agent.name);        // display name
    gs.info('Agent phone:   ' + order.agent.getValue('phone'));
}
```

Dot-walking follows the relationship without a second query — one of the most powerful (and commonly misused) features.

## Count Records in a Table

```js
var agents = new GlideRecord('u_delivery_agents');
agents.query();
var count = agents.getRowCount();       // number of matching records
gs.info('Total agents: ' + count);
```

`getRowCount()` only works after `query()` and counts the result set.

## Lab: List the GlidePort Fleet

1. Open **Scripts Background**.
2. Query `u_delivery_agents` and log every agent's name and phone:
   ```js
   var agents = new GlideRecord('u_delivery_agents');
   agents.query();
   while (agents.next()) {
       gs.info(agents.getValue('name') + ' | ' + agents.getValue('phone'));
   }
   ```
3. Fetch one order by number and log its status.
4. Use dot-walking to log the agent name for one order (if your table has an agent reference field).
5. Log the total number of agents with `getRowCount()`.

## Key Takeaways

- `GlideRecord` is the server-side API to query table records.
- `get()` loads one record by value or sys_id; `query()` + `next()` iterates many.
- `getValue()` returns field values as strings; dot-walking follows reference fields.
- `getRowCount()` counts the result set after `query()`.
- Always check the return of `get()` before using the record.
