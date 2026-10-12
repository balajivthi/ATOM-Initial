# Client Script Patterns

**Story so far:** The Delivery App form now reacts — fields hide, values cascade, saves get validated. These wins came from three classic patterns. This lesson collects the patterns you'll reuse on *every* form you ever build.

## Pattern 1 — Show/Hide (cascading fields)

React to one field's value by showing or hiding related fields.

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    var isUrgent = newValue === 'priority';
    g_form.setDisplay('u_delivery_date', isUrgent);
    g_form.setDisplay('u_urgency', isUrgent);
}
```

**Use it for:** optional sections that only matter for some records (a "hazardous" checkbox revealing hazmat fields).

## Pattern 2 — Mandatory toggling

Make a field required only under certain conditions.

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    g_form.setMandatory('u_return_reason', newValue === 'returned');
}
```

**Use it for:** collecting extra info exactly when it's needed — without annoying everyone else.

## Pattern 3 — Copy / derive a value

Populate one field from another so agents stop re-typing.

```js
function onLoad() {
    var orderNumber = g_form.getValue('u_order_number');
    if (orderNumber) {
        g_form.setValue('u_display_label', 'Order ' + orderNumber);
    }
}
```

**Use it for:** derived labels, audit names, or defaulting a field from the parent record.

## Pattern 4 — Clear dependent values

When a parent changes, reset fields that no longer make sense.

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading) {
        return;
    }
    if (oldValue !== newValue) {
        g_form.clearValue('u_agent');
        g_form.clearValue('u_urgency');
    }
}
```

**Use it for:** preventing stale data — e.g. clearing the assigned agent when the route changes.

## Pattern 5 — Input cleaning & formatting

Normalize values as the user types or before save.

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    g_form.setValue(control.name, newValue.trim().toUpperCase());
}
```

**Use it for:** uppercase tracking codes, trimming whitespace, stripping dashes from phone numbers.

## Pattern 6 — Confirmation before destructive action

Acknowledge important changes on submit.

```js
function onSubmit() {
    if (g_form.getValue('u_priority') === 'priority') {
        return confirm('This order is priority. Continue?');
    }
    return true;
}
```

**Use it for:** "are you sure?" on irreversible or high-impact updates. Don't overuse — confirmations get ignored when they appear everywhere.

## Pattern 7 — Validate across fields

Checks that span more than one field (single-field checks can stay in UI Policies).

```js
function onSubmit() {
    var agent = g_form.getValue('u_agent');
    var urgency = g_form.getValue('u_urgency');
    if (urgency === 'high' && !agent) {
        g_form.addErrorMessage('A priority order needs an assigned agent.');
        return false;
    }
    return true;
}
```

## When to Reach for a Server-Side Rule Instead

| Need | Where it belongs |
| --- | --- |
| Show/hide, readonly, mandatory | Client Script or UI Policy |
| Validation the user must see instantly | Client Script (`onSubmit`) |
| Validation that must **always** happen | **Business Rule** (server) |
| Values only the server can know | **Business Rule** / Script Include |
| Security (who can see/edit) | **ACLs** — never client-side |

Client Scripts make the UI friendly. Server rules make it correct. **Build both.**

## Debugging Toolkit

- Browser console (`F12`) — errors + `console.log()`.
- `g_form.log('value', field)` writes to the console with field context.
- Network tab — confirm no accidental server calls.
- `g_form.setVisible` vs `setDisplay`: prefer `setDisplay` (handles the label too).

## Key Takeaways

- Seven small patterns cover most Client Script needs: show/hide, mandatory, derive, clear, clean, confirm, cross-field validate.
- Always pair client-side validation with server-side rules.
- `g_form` is the API; browser console is your debugger.
- Simple rules → UI Policies. Real logic → Client Scripts. Truth → server.
