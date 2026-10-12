# The AJAX Lab

**Story so far:** GlidePort's agents want to type an order number on the Delivery form and see the live status — no save, no reload, no page jump. You'll build that end-to-end: a client-callable Script Include on the server, a Client Script in the browser, and a live test.

## What You're Building

**"Status Peek"** — type an order number into a field, and a status panel fills in from the server instantly.

## Step 1 — The client-callable Script Include

Create a Script Include:

- **Name:** `OrderStatusAjax`
- **API name:** `OrderStatusAjax`
- **Client callable:** ✔ checked
- **Script:**

```js
var OrderStatusAjax = Class.create();

OrderStatusAjax.prototype = Object.extendsObject(AbstractAjaxProcessor, {

    getStatus: function() {
        var orderNumber = this.getParameter('sysparm_order_number');
        if (!orderNumber) {
            return JSON.stringify({ found: false, reason: 'no number' });
        }
        var gr = new GlideRecord('u_order_tracking');
        if (!gr.get('number', orderNumber)) {
            return JSON.stringify({ found: false, reason: 'not found' });
        }
        return JSON.stringify({
            found: true,
            status: gr.getValue('status'),
            urgency: gr.getValue('u_urgency') || '—',
            agent: gr.getValue('u_agent') || '—'
        });
    },

    type: 'OrderStatusAjax'
});
```

**Check your work (server-side):** in Scripts Background:

```js
var ajax = new GlideAjax('OrderStatusAjax');
ajax.addParam('sysparm_name', 'getStatus');
ajax.addParam('sysparm_order_number', 'ORD0010001');
gs.print(ajax.getXML());
```

(`getXML()` is the server-side version of the browser's async call — great for debugging.)

## Step 2 — The Client Script

Create a Client Script on `u_order_tracking`:

- **Name:** `Status peek on order number`
- **Table:** `u_order_tracking`
- **Type:** `onChange`
- **Field name:** `u_order_number`

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    var ga = new GlideAjax('OrderStatusAjax');
    ga.addParam('sysparm_name', 'getStatus');
    ga.addParam('sysparm_order_number', newValue);
    ga.getXMLAnswer(function(answer) {
        var snap = JSON.parse(answer);
        if (!snap.found) {
            g_form.addErrorMessage('No delivery found for ' + newValue + '.');
            return;
        }
        g_form.setValue('u_status_display', snap.status);
        g_form.setValue('u_urgency', snap.urgency);
        g_form.addInfoMessage(
            'Order ' + newValue + ' is ' + snap.status + ' — agent ' + snap.agent
        );
    });
}
```

Make sure `u_order_number` and `u_status_display` exist on your table (add `u_status_display` as a read-only string field if needed).

## Step 3 — Test the Full Round Trip

1. Open a delivery record in the **list or form**.
2. Change the **Order Number** to a real order.
3. Watch the status message appear **without saving** — the Network tab shows a single async call (`XMLHttpRequest`), not a page reload.
4. Try a fake order number and confirm the friendly error.

## Step 4 — Extend It (choose one)

- **Search history:** add a `getHistory()` method returning the last 5 statuses as JSON, and render them in the message.
- **Validate before save:** call the ajax in `onSubmit` (using a synchronous flow via `getXML()`), block the save if the order number isn't found.
- **Guard it:** wrap the record lookup in a permission check so only agents with a role see the status.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Answer is `false`/empty | Method name in `sysparm_name` doesn't match; or **Client callable** is unchecked |
| `undefined` fields | The JSON key doesn't exist — check the server method's return |
| CORS / blocked | Wrong instance URL in your test script — use the same instance |
| Still reloads | You edited a different Client Script than the one attached to the table |

## Key Takeaways

- Two files, one round trip: **Script Include** (server, client-callable) + **Client Script** (browser, GlideAjax).
- Test the include alone in Scripts Background before wiring the UI.
- Return JSON, parse in the callback, handle "not found" gracefully.
- This same pattern powers countless portal widgets and dashboard gadgets.
