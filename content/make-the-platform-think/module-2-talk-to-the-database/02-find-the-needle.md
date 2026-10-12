# Find the Needle

**Story so far:** Reading every agent is fine, but GlidePort needs answers: *Which orders are urgent? What's the current fleet size?* That's **filtering** and **aggregation** — and GlideRecord makes it easy.

## Filtering with `addQuery()`

`addQuery(field, operator, value)` adds a condition to the query:

```js
var urgent = new GlideRecord('u_order_tracking');
urgent.addQuery('urgent', true);          // only urgent orders
urgent.query();

while (urgent.next()) {
    gs.info('Urgent: ' + urgent.getValue('number'));
}
```

Operators are the same ideas you saw in lists: `=`, `!=`, `>`, `<`, `>=`, `<=`, `STARTSWITH`, `CONTAINS`, `IN`, and more.

```js
var old = new GlideRecord('u_order_tracking');
old.addQuery('created_on', '<', gs.daysAgoStart(7));  // created over a week ago
old.query();
```

### Chaining multiple conditions (AND)

```js
var fleet = new GlideRecord('u_delivery_agents');
fleet.addQuery('status', 'active');
fleet.addQuery('city', 'Chennai');
fleet.query();
```

Both conditions must match — that's an **AND**.

### OR conditions

```js
var q = new GlideRecord('u_delivery_agents');
q.addQuery('status', 'active').addOrCondition('status', 'on_break');
q.query();
```

## Active-Only Shortcuts

Most business tables extend the **Task** table and have an **Active** flag:

```js
var open = new GlideRecord('task');
open.addActiveQuery();         // equivalent to addQuery('active', true)
```

## Ordering Results

```js
var agents = new GlideRecord('u_delivery_agents');
agents.orderBy('name');        // ascending
agents.orderByDesc('joined_on'); // descending
agents.query();
```

## Aggregates Without Pulling Every Row

GlideRecord can count, sum, min and max **in the database** — no loop needed:

```js
// Count
var fleet = new GlideRecord('u_delivery_agents');
fleet.addQuery('status', 'active');
fleet.query();
var count = fleet.getRowCount();

// Sum a numeric field
var orders = new GlideRecord('u_order_tracking');
var sum = orders.get('?');        // placeholder — see below
```

### Aggregate via `getAggregate()`

For sums/averages/min/max, use the aggregate API:

```js
var orders = new GlideRecord('u_order_tracking');
var total = orders.getAggregate('SUM', 'weight_kg');
gs.info('Total weight of all orders: ' + total);
```

Other aggregates: `AVG`, `MIN`, `MAX`, `COUNT`.

> Aggregates run server-side, so they scale even with huge tables — much better than summing in a loop.

## Combining Filters with Aggregates

```js
var urgent = new GlideRecord('u_order_tracking');
urgent.addQuery('urgent', true);
var urgentTotal = urgent.getAggregate('COUNT');
gs.info('Urgent orders: ' + urgentTotal);
```

## Dot-Walking in Queries

You can filter on **related** fields:

```js
var q = new GlideRecord('u_order_tracking');
q.addQuery('agent.city', 'Chennai');   // orders whose agent is in Chennai
q.query();
```

## Lab: GlidePort Fleet Report

1. Log all **active** agents ordered by name.
2. Log the **count** of active agents.
3. Log orders that are **urgent** (add a `urgent` boolean column to Order & Tracking if you don't have one).
4. Sum the `weight_kg` column (add it if missing) across all orders using `getAggregate('SUM', 'weight_kg')`.
5. Filter orders where the agent is in a specific city using dot-walking.

## Key Takeaways

- `addQuery(field, op, value)` filters; chain conditions for AND, `addOrCondition` for OR.
- `addActiveQuery()` is the shortcut for active records on Task-based tables.
- `orderBy` / `orderByDesc` sort results.
- `getRowCount()` and `getAggregate('SUM'|'AVG'|'MIN'|'MAX'|'COUNT')` do work in the database, not in loops.
- Dot-walking in `addQuery` filters on related-table fields.
