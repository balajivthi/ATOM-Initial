# The AJAX Pattern

**Story so far:** Agents keep saving and reopening delivery records just to check the status of an order. Annoying — and it's pure server work that doesn't need a form save. What if the browser could **ask the server a quick question and update the page live**? That's exactly what **GlideAjax** does.

## The Pattern in One Sentence

A **client-callable Script Include** is a server-side class the browser can call with `GlideAjax`, returning a value the Client Script uses to update the form — no reload, no save.

## Step 1 — The Server Side: a Client-Callable Script Include

Mark a Script Include as **Client callable** and extend **`AbstractAjaxProcessor`**. Every method you want the browser to call is a function that can read request params with `this.getParameter('sysparm_...')`:

```js
var OrderLookup = Class.create();

OrderLookup.prototype = Object.extendsObject(AbstractAjaxProcessor, {

    // Returns the current status of a delivery order
    getStatus: function() {
        var orderNumber = this.getParameter('sysparm_order_number');
        var gr = new GlideRecord('u_order_tracking');
        if (gr.get('number', orderNumber)) {
            return gr.getValue('status');
        }
        return 'not found';
    },

    type: 'OrderLookup'
});
```

Remember to check the **Client callable** checkbox.

## Step 2 — The Client Side: GlideAjax

From a Client Script, call the include by name, pass params, and handle the answer in a **callback**:

```js
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue === '') {
        return;
    }
    var ga = new GlideAjax('OrderLookup');
    ga.addParam('sysparm_name', 'getStatus');       // which method
    ga.addParam('sysparm_order_number', newValue);  // your data
    ga.getXMLAnswer(function(answer) {
        g_form.setValue('u_status_display', answer);
        g_form.addInfoMessage('Current status: ' + answer);
    });
}
```

## Rules of the Road

| Rule | Why |
| --- | --- |
| Param names start with `sysparm_` | Platform convention; the server reads them via `this.getParameter` |
| You must pass `sysparm_name` | Tells the server which method to run |
| The callback is **async** | The page keeps working; the answer arrives later |
| Return **strings** (or JSON) | `getXMLAnswer` gives you text back |
| Runs **as the current user** | ACLs and roles still apply server-side — don't leak data |
| Keep methods **fast** | They run on every relevant keystroke/change |

## Returning More Than a String

Return a JSON string and parse it in the callback for richer results:

```js
// server
getSnapshot: function() {
    var orderNumber = this.getParameter('sysparm_order_number');
    var gr = new GlideRecord('u_order_tracking');
    if (!gr.get('number', orderNumber)) {
        return JSON.stringify({ found: false });
    }
    return JSON.stringify({
        found: true,
        status: gr.getValue('status'),
        agent: gr.getValue('u_agent'),
        urgency: gr.getValue('u_urgency')
    });
}
```

```js
// client
var ga = new GlideAjax('OrderLookup');
ga.addParam('sysparm_name', 'getSnapshot');
ga.addParam('sysparm_order_number', newValue);
ga.getXMLAnswer(function(answer) {
    var snap = JSON.parse(answer);
    if (snap.found) {
        g_form.setValue('u_urgency', snap.urgency);
    }
});
```

## When NOT to Use GlideAjax

- **Many rows of data** → use a server-side page, an aggregate, or a scripted REST API instead of chatty Ajax calls.
- **Security-critical reads** → still guard with ACLs; GlideAjax runs as the user but returns exactly what you code it to return.
- **Pure client-side logic** → don't round-trip; just compute in the browser.

## Best Practices

- Name params consistently (`sysparm_order_number` matches the method's need).
- Always handle the "not found" case with a sensible return, never an exception.
- Validate inside the server method — treat the browser as hostile input.
- Keep one method per concern; a giant ajax processor is a maintenance trap.

## Key Takeaways

- **GlideAjax** = browser → server → answer, async, no reload.
- Server side is a **client-callable Script Include** extending `AbstractAjaxProcessor`; read input via `this.getParameter('sysparm_...')`.
- Client side passes `sysparm_name` + data and uses `getXMLAnswer(callback)`.
- Returns strings or JSON; always runs as the current user with ACLs enforced.
