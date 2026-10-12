# Meet the Client Script

**Story so far:** Business Rules gave the Delivery App a server-side brain — statuses auto-set, order processing automated. But GlidePort's agents still fight the *form*: they type, re-type, and fix mistakes in the browser. The team wants the form itself to be smart — show the right fields, validate input, auto-fill. No server trip required.

## What is a Client Script?

A **Client Script** is JavaScript that runs in the **user's browser** on a form — the opposite of a Business Rule, which runs on the server. Client Scripts make the form behave: hide fields, validate values, auto-complete fields, and confirm actions.

They use the **`g_form`** API (the "form object"), which knows every field on the current form.

> **Key difference:** Business Rules run server-side and *always* run. Client Scripts run in the browser and can be skipped (bad network, disabled JS). **Never trust client-side code for security** — that's what ACLs and server rules are for.

## The Three Events

A Client Script picks one event that triggers it:

| Event | When it runs | Typical use |
| --- | --- | --- |
| **onLoad** | When the form opens | Show/hide fields based on the record, prefill values, set defaults |
| **onChange** | When a specific field changes | React to a field value — cascade show/hide, recompute, warn |
| **onSubmit** | When the form is submitted | Validate, confirm, block bad saves |

## Meet `g_form`

The `g_form` API is the bread and butter of Client Scripts:

```js
function onLoad() {
    g_form.setDisplay('u_internal_notes', false);   // hide a field
    g_form.setValue('u_priority', 'standard');       // set a value
    g_form.setReadOnly('u_agent', true);             // lock a field
}

function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    // 'control' is the field that changed — here's the field name
    var field = control.name;
    g_form.setMandatory('u_delivery_date', newValue === 'true');
}

function onSubmit() {
    if (!g_form.getValue('u_order_number')) {
        g_form.addErrorMessage('Order number is required.');
        return false;   // blocks the save
    }
    return true;
}
```

Common `g_form` methods you'll use every day:

| Method | What it does |
| --- | --- |
| `g_form.getValue('field')` | Read a field's value |
| `g_form.setValue('field', 'value')` | Set a field's value |
| `g_form.setDisplay('field', bool)` | Show/hide a field |
| `g_form.setMandatory('field', bool)` | Make a field required/optional |
| `g_form.setReadOnly('field', bool)` | Lock/unlock a field |
| `g_form.addErrorMessage('msg')` | Show an error banner |
| `g_form.addInfoMessage('msg')` | Show an info banner |
| `g_form.getControl('field')` | Get the raw DOM element (for styling) |

## Client Scripts vs UI Policies

| | **Client Script** | **UI Policy** |
| --- | --- | --- |
| Runs in | Browser | Browser |
| Build method | Code | Point-and-click (also generates code) |
| Good for | Complex logic, validation, calculations | Simple show/hide/mandatory/readonly rules |
| Needs a reload | Sometimes (onLoad) | No — reactive by design |

Rule of thumb: start with a **UI Policy**; reach for a **Client Script** when you need real logic — loops, conditions across many fields, calculations, or validation with messages.

## Creating One in Studio

1. **All → System Definition → Client Scripts → New**
2. Set **Table** to the form's table (e.g. `u_order_tracking`).
3. Set **Type** to `onLoad`, `onChange`, or `onSubmit`.
4. For `onChange`, pick the **Field name** that triggers it.
5. Write the script and **Update**.

## Best Practices

- Always guard `onChange` with the `isLoading` early-return so it doesn't fire while the form is still loading.
- Use `g_form.addErrorMessage` + `return false` for validation in `onSubmit`.
- Keep logic small — push heavy work to server-side (Script Includes, covered next course).
- Remember: **client-side is convenience, server-side is truth.** ACLs decide who may *actually* see or edit data.

## Key Takeaways

- Client Scripts run in the browser via the `g_form` API.
- Three events: **onLoad**, **onChange**, **onSubmit**.
- `g_form` reads/writes values and controls visibility, required state, and readonly.
- Simple show/hide → UI Policy; real logic → Client Script.
- Never rely on Client Scripts for security.
