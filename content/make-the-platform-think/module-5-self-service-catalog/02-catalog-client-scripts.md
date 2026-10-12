# Catalog Client Scripts

**Story so far:** "Report a Delivery Issue" is live, but the form is dumb — it shows every question to everyone, even when it makes no sense. A customer reporting a *late* delivery shouldn't be asked to upload damage photos. Time to make the catalog form react, the same way Client Scripts made the Delivery App form react.

## What Is a Catalog Client Script?

A **Catalog Client Script** is a Client Script that runs on a **catalog item or variable set** in the browser — `onLoad`, `onChange`, and `onSubmit`, just like a normal Client Script. The API is still **`g_form`**, but there's a twist: **catalog variables are referenced with a `variable_` prefix**.

```js
// Regular form field → g_form.getValue('u_order_number')
// Catalog variable  → g_form.getValue('variable_order_number')
```

So the catalog question **Order Number** (variable name `order_number`) is `variable_order_number` in scripts.

## The `catalyst` API

Modern catalog client scripts can also use the **`catalyst`** object — a catalog-aware wrapper over `g_form`:

```js
catalyst.getValue('order_number');       // note: no variable_ prefix
catalyst.setValue('details', '...');
catalyst.setMandatory('order_number', true);
catalyst.setVisible('include_photo', false);
```

`catalyst` hides the `variable_` prefix and is the friendlier choice for catalog scripts. Both work — pick one per script and stay consistent.

## Where They Attach

Catalog Client Scripts attach to:

- **A single catalog item** — script only runs on that item.
- **A variable set** — script runs on *every* item that includes the variable set (great for reuse: a "billing address" set with its own logic).

## Typical Examples

### Show a field only for one issue type

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    // issue_type = damaged | missing | late
    var askForPhoto = newValue === 'damaged';
    catalyst.setVisible('include_photo', askForPhoto);
    catalyst.setMandatory('include_photo', askForPhoto);
}
```

### Make one variable required based on another

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading) {
        return;
    }
    // A "missing" delivery must include the last known location
    catalyst.setMandatory('last_seen_location', newValue === 'missing');
}
```

### Validate on submit

```js
function onSubmit() {
    if (catalyst.getValue('issue_type') === 'late' &&
        !catalyst.getValue('order_number')) {
        g_form.addErrorMessage('Order Number is required for late deliveries.');
        return false;
    }
    return true;
}
```

## Client Script vs Catalog Client Script

| | **Client Script** | **Catalog Client Script** |
| --- | --- | --- |
| Runs on | Table forms | Catalog items / variable sets |
| API | `g_form` | `g_form` + `catalyst` |
| Field access | Plain field names | `variable_<name>` or `catalyst.getValue('name')` |
| Attach to | Table + event | Item / variable set + event |

## Best Practices

- Use `catalyst` for readability; keep `variable_` in mind when reading existing scripts.
- Guard `onChange` with the `isLoading` early-return.
- Put reusable logic on a **variable set** so every item inherits it.
- Only make variables mandatory when the *context* demands it — mandatory-everything kills self-service.
- Still validate server-side (Record Producer / Business Rule) — the portal browser is not the source of truth.

## Key Takeaways

- Catalog Client Scripts are Client Scripts for catalog items — same three events, same `g_form`.
- Catalog variables use the `variable_<name>` prefix (or the `catalyst` API).
- Attach to a single item for one-off logic, or a variable set for reuse.
- Same rules as everywhere: guard `onChange`, validate on submit, trust the server.
