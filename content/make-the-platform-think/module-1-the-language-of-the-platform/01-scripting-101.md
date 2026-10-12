# Scripting 101

**Story so far:** You joined GlidePort Logistics and set up the Delivery App — `Order & Tracking` and `Delivery Agents` tables, import, notifications, catalog. It works, but every rule so far was manual configuration. Now GlidePort wants the app to *think*: auto-set statuses, validate deliveries, and speak to other systems.

That thinking runs on **JavaScript** — the language of the platform. This lesson covers the essentials you'll use every day.

## Why JavaScript on ServiceNow?

ServiceNow scripts run JavaScript in two places:

- **Server-side** — on the platform's servers (Business Rules, Script Includes, scheduled jobs). Uses Glide APIs like `GlideRecord`.
- **Client-side** — in the user's browser (Client Scripts, UI Policies). Uses the `glideForm` object.

The language is the same; the **APIs** differ. You'll start with pure JavaScript so the fundamentals are solid before touching platform APIs.

## Variables and Data Types

```js
// Strings, numbers, booleans — the basics
var name = 'GlidePort';        // string
var fleetSize = 42;            // number
var isActive = true;           // boolean

// Arrays hold lists of values
var agents = ['Ana', 'Bo', 'Chi'];

// Objects group related values
var order = {
    number: 'ORD0010001',
    status: 'new',
    urgent: false
};
```

- Variables are declared with `var` (older style, still everywhere in ServiceNow code) or `let`/`const`.
- Use `===` for strict equality and `!==` for inequality — never `==`/`!=` (type coercion causes bugs).

## Functions

Functions package logic so you can reuse it:

```js
function isUrgent(order) {
    return order.urgent === true;
}

function describe(order) {
    if (isUrgent(order)) {
        return 'Priority delivery ' + order.number;
    }
    return 'Standard delivery ' + order.number;
}
```

### Arrow functions

Modern and compact:

```js
var isUrgent = (order) => order.urgent === true;
var describe = (order) => isUrgent(order) ? 'Priority ' + order.number : 'Standard ' + order.number;
```

## Conditionals and Loops

```js
// Conditionals
if (order.status === 'delivered') {
    gs.info('Order delivered: ' + order.number);
} else if (order.status === 'new') {
    gs.info('Order is new.');
} else {
    gs.info('Order in progress.');
}

// Loops over an array
for (var i = 0; i < agents.length; i++) {
    gs.info('Agent: ' + agents[i]);
}

// for...of (cleaner)
for (var agent of agents) {
    gs.info('Agent: ' + agent);
}
```

> **Note:** `gs.info()` is the platform's logging method (covered in the next lesson). Logging is your best friend while learning.

## Working with Objects

```js
var order = { number: 'ORD0010001', status: 'new' };

// Read values
var num = order.number;          // 'ORD0010001'

// Write values
order.status = 'packed';

// Add new properties
order.weightKg = 12.5;

// Loop over keys
for (var key in order) {
    gs.info(key + ' = ' + order[key]);
}
```

## Common Pitfalls for Beginners

| Pitfall | Why it's wrong | Fix |
| --- | --- | --- |
| Using `==` instead of `===` | `'1' == 1` is true but they differ in type | Always `===` |
| Forgetting `var`/`let` | Creates a global by accident | Declare variables explicitly |
| Off-by-one in `for` loops | Indexes start at 0 | Loop `i < arr.length` |
| Modifying an object while iterating | Unexpected results | Build a new object instead |

## Lab: Your First Data Model in Code

Write a small script that models GlidePort's delivery workflow:

1. Create an `order` object with `number`, `status`, and `isPriority`.
2. Write a function `nextStatus(order)` that returns the next step: `new → packed → shipped → delivered`.
3. Loop over an array of 3 orders and log each order's current status and next status.

**Check your work:** run it in the Scripts Background editor (see next lesson) and confirm each order logs correctly.

## Key Takeaways

- ServiceNow scripts are JavaScript — server-side or client-side.
- Master variables, functions, conditionals, loops and objects first.
- Use `===`, declare variables, and log with `gs.info()`.
- In the next lesson you'll run these scripts inside ServiceNow itself.
