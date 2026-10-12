# Your First Client Script

**Story so far:** The Delivery App form is boring and error-prone. Agents keep entering "priority" deliveries without an urgency value, and internal notes are visible to people who shouldn't see them. Let's fix the form in the browser — three small Client Scripts, one per event.

## Setup

All three scripts below attach to the **`u_order_tracking`** table. In this course the table has (at least) these fields:

| Field | Type |
| --- | --- |
| `number` | Order number (auto, system) |
| `u_priority` | Choice: standard / priority |
| `u_urgency` | Choice: low / medium / high |
| `u_delivery_date` | Date/time |
| `u_internal_notes` | Text |
| `u_agent` | Reference → Delivery Agents |

## Lab 1 — onLoad: hide what's not yours

**Goal:** Hide `u_internal_notes` from agents who aren't admins or supervisors.

Create a Client Script:

- **Name:** `Hide internal notes on load`
- **Table:** `u_order_tracking`
- **Type:** `onLoad`

```js
function onLoad() {
    if (!g_user.hasRole('admin') && !g_user.hasRole('u_supervisor')) {
        g_form.setDisplay('u_internal_notes', false);
    }
}
```

`g_user` is the current user's browser-side object — `hasRole()` tells you their roles without a server call.

**Check your work:** open a delivery record as a non-supervisor and confirm the field is gone; open it as an admin and confirm it's back.

## Lab 2 — onChange: react to a priority delivery

**Goal:** When an agent marks an order as **priority**, auto-set urgency to **high** and make the delivery date mandatory; when it's back to standard, loosen both.

Create a Client Script:

- **Name:** `Priority delivery handling`
- **Table:** `u_order_tracking`
- **Type:** `onChange`
- **Field name:** `u_priority`

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    if (newValue === 'priority') {
        g_form.setValue('u_urgency', 'high');
        g_form.setMandatory('u_delivery_date', true);
        g_form.addInfoMessage('Priority delivery — schedule a date.');
    } else {
        g_form.setMandatory('u_delivery_date', false);
    }
}
```

**Check your work:** flip the priority field and watch urgency change live — no reload, no server round trip.

## Lab 3 — onSubmit: validate before saving

**Goal:** Block the save if the delivery date is in the past, or the agent left the order number field blank.

Create a Client Script:

- **Name:** `Validate delivery details`
- **Table:** `u_order_tracking`
- **Type:** `onSubmit`

```js
function onSubmit() {
    var date = g_form.getValue('u_delivery_date');
    var number = g_form.getValue('u_order_number');

    if (!number) {
        g_form.addErrorMessage('Order number is required.');
        return false;
    }
    if (date && new Date(date) < new Date()) {
        g_form.addErrorMessage('Delivery date cannot be in the past.');
        return false;
    }
    return true;
}
```

Returning `false` cancels the save and shows your message.

**Check your work:** submit a blank order number and a past date — the form refuses to save and explains why.

## How to Debug

- Open **developer console** (F12 → Console) — Client Script errors and `console.log()` output appear there.
- Add `console.log('priority is', newValue);` in `onChange` while testing.
- The browser's Network tab shows you every server call — confirm nothing fires when scripts do their work.

## Best Practices

- One script = one job; don't cram onLoad logic into onChange.
- Use the `isLoading` guard in every `onChange`.
- Validate in `onSubmit` and *also* server-side (a Business Rule) — the browser is not the source of truth.
- Prefer `g_form` methods over raw DOM (`document.getElementById`) — they survive UI updates like Next Experience.

## Key Takeaways

- Three small scripts — onLoad, onChange, onSubmit — already transform the form.
- `g_user.hasRole()` gates UI behaviour without a server call.
- `g_form.setMandatory` + `addErrorMessage` + `return false` is the standard validation pattern.
- Debug in the browser console; validate server-side too.
