# Script Includes Unplugged

**Story so far:** You've written Business Rules that set statuses, Client Scripts that polish forms, and catalog scripts that guide customers. The Delivery App works — but the same snippets keep reappearing: "next status", "is this urgent?", "format the tracking code". Every duplicate is a future bug. Time to write that logic **once** and reuse it everywhere.

## What Is a Script Include?

A **Script Include** is a server-side, reusable library of code. Think of it as a **class** you write once and `new` up anywhere — Business Rules, other Script Includes, scheduled jobs, even REST endpoints.

They live in the table **`sys_script_include`** (`All → System Definition → Script Includes → New`).

## Anatomy of a Script Include

```js
var DeliveryUtils = Class.create();

DeliveryUtils.prototype = Object.extendsObject(AbstractAjaxProcessor, {

    // A simple method that returns the next status in the workflow
    nextStatus: function(currentStatus) {
        var steps = ['new', 'packed', 'shipped', 'delivered'];
        var i = steps.indexOf(currentStatus);
        if (i === -1 || i === steps.length - 1) {
            return null;
        }
        return steps[i + 1];
    },

    isUrgent: function(orderGr) {
        return orderGr.getValue('u_priority') === 'priority';
    },

    type: 'DeliveryUtils'
});
```

Using it from a Business Rule:

```js
(function executeRule(current, previous) {
    var utils = new DeliveryUtils();
    if (utils.isUrgent(current)) {
        current.setValue('u_urgency', 'high');
    }
})(current, previous);
```

## Key Settings

| Setting | What it controls |
| --- | --- |
| **Name** | The class name you `new` up (e.g. `DeliveryUtils`) |
| **API name** | Auto-derived, used by REST/SOAP and GlideAjax |
| **Client callable** | Off = server-only; **On** = callable from the browser via GlideAjax (next lesson) |
| **Accessible from** | Which application scope may use it (App Scope, Global, etc.) |

> **Note:** the example extends `AbstractAjaxProcessor` — that's what makes a Script Include *client-callable*. You don't need it for server-only includes; extend `Class.create()` directly.

## Why Script Includes Matter

- **One copy of the truth** — fix a formula in one place, every rule picks it up.
- **Tiny Business Rules** — rules become two lines that call a tested method.
- **Testable** — run a method directly in Scripts Background:
  ```js
  var utils = new DeliveryUtils();
  gs.print(utils.nextStatus('packed'));   // -> shipped
  ```
- **Foundation for everything ahead** — REST endpoints and client-callable code (this course) both lean on Script Includes.

## Lab: Consolidate the Delivery Logic

Collect the logic you've scattered across Business Rules into one include.

1. Create `DeliveryUtils` as above.
2. Move the "set urgency for priority orders" logic from your Business Rule into `DeliveryUtils.isUrgent()` and have the rule call it.
3. Add a method `formatTrackingCode(code)` that uppercases and strips spaces.
4. Test in Scripts Background: `gs.print(new DeliveryUtils().formatTrackingCode(' ab 12 '));` → `AB12`.

**Check your work:** the Business Rule now contains zero duplicated logic and the same method is reusable from any future script.

## Best Practices

- Keep methods **small** and **side-effect free** where possible — pass data in, return data out.
- Give the class a **clear domain name** (`DeliveryUtils`, not `Utils`).
- Don't store per-request state in instance variables — Script Includes can be instantiated anywhere.
- Cache expensive lookups (system properties, config) inside the method with a local variable.
- Mark it **client callable only when needed** — every exposed method is an attack surface.

## Key Takeaways

- Script Includes are server-side **classes** for reusable logic.
- Business Rules call them, staying tiny and consistent.
- `Client callable` + `AbstractAjaxProcessor` turns one into a browser-facing service (next lesson).
- One source of truth → fewer bugs, easier testing.
