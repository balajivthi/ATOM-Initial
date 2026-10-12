# Catalog Client Script Lab

**Story so far:** "Report a Delivery Issue" exists but asks everyone everything. In this lab you'll make it a smart form end-to-end: extra variables for damaged/missing cases, a visible-only-when-needed photo field, and a submit-time validation. Then you'll prove it works in the portal.

## The Target Behaviour

A customer reports a delivery issue:

- **Late** deliveries → must provide the **Order Number** (so we can chase it).
- **Missing** deliveries → must provide **Last Seen Location**.
- **Damaged** deliveries → must answer **Include a Photo**.
- Anything else → keep the form short.

## Step 1 — Extend the catalog item

Open **Report a Delivery Issue** (Catalog item) and add these variables:

| Name | Label | Type | Notes |
| --- | --- | --- | --- |
| `order_number` | Order Number | Reference → `u_order_tracking` | Required (we'll script it for late) |
| `issue_type` | Issue Type | Choice | damaged / missing / late |
| `details` | Describe the Issue | Multi-line text | Required |
| `last_seen_location` | Last Seen Location | Single line text | Hidden by default |
| `include_photo` | Include a Photo | Checkbox | Hidden by default |

Update the item.

## Step 2 — onChange: react to the issue type

**All → System Definition → Catalog Client Scripts → New**

- **Name:** `Issue type rules`
- **Catalog Item:** Report a Delivery Issue
- **Type:** `onChange`
- **Variable name:** `issue_type`

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    // Late: order number is mandatory
    catalyst.setMandatory('order_number', newValue === 'late');
    // Missing: reveal + require last seen location
    catalyst.setVisible('last_seen_location', newValue === 'missing');
    catalyst.setMandatory('last_seen_location', newValue === 'missing');
    // Damaged: reveal the photo question
    catalyst.setVisible('include_photo', newValue === 'damaged');
}
```

**Check your work:** switch issue types and watch the relevant fields appear and become required — no reload.

## Step 3 — onSubmit: validate before ordering

- **Name:** `Validate delivery issue report`
- **Catalog Item:** Report a Delivery Issue
- **Type:** `onSubmit`

```js
function onSubmit() {
    var issue = catalyst.getValue('issue_type');
    if (issue === 'late' && !catalyst.getValue('order_number')) {
        g_form.addErrorMessage('Late deliveries need an Order Number.');
        return false;
    }
    if (issue === 'missing' && !catalyst.getValue('last_seen_location')) {
        g_form.addErrorMessage('Where did you last see the delivery?');
        return false;
    }
    return true;
}
```

**Check your work:** try submitting a "late" report without an order number — the portal refuses and explains why.

## Step 4 — Test the whole flow in the Service Portal

1. Open the Service Portal home and search **Report a Delivery Issue**.
2. Order it as a customer: choose **late**, fill in the order number + details, submit.
3. Check the **Request** was created (`All → My Requests` as the requester).
4. Repeat with **missing** and **damaged** and confirm the right fields appeared each time.

## Step 5 — (Optional) Land it in the Delivery App

Wire a **Record Producer** to `Report a Delivery Issue` so a successful report creates a row on `u_order_tracking` (a new "issue" status) instead of just a Request. Reuse your Business Rule knowledge: set the status, copy the variable values onto the record, and let the platform handle the rest.

## Debrief

| What you built | Which skill it used |
| --- | --- |
| Conditional visibility | Catalog Client Script (`onChange` + `catalyst.setVisible`) |
| Conditional requirements | `catalyst.setMandatory` |
| Validation | `onSubmit` + `addErrorMessage` + `return false` |
| Data landing in a table | Record Producer + variables |

## Key Takeaways

- A catalog form becomes smart with three small Catalog Client Scripts.
- `catalyst` + `onChange` = the form reacts; `onSubmit` = the form refuses bad input.
- Test as the *requester* in the Service Portal, not just in the admin UI.
- End-to-end = item → variables → scripts → Record Producer → your table.
