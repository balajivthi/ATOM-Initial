# Your First Outbound Call

**Story so far:** The integration map is on the wall, and the first arrow points *out* — GlidePort needs to ask the van partner for a parcel's status. Time to make that call for real.

## Two Ways to Call Out

| Approach | Built with | Best for |
| --- | --- | --- |
| **REST Message** (declarative) | A record you configure, no code | A stable partner API you'll call often — reuse and share |
| **Scripted REST call** | `RESTMessageV2` in server-side JS | One-off calls, dynamic URLs, logic before the call |
| **Flow REST step / spoke action** | Flow Designer, drag-and-drop | No-code automation (Module 4) |

We'll learn the declarative record first — it's the one you'll reuse — then the scripted form.

## Build a REST Message

1. **All → System Web Services → Outbound → REST Message → New**.
2. **Name:** `GlidePort Shipping`
3. **Endpoint:** `https://dummyjson.com`  *(the partner sandbox — see [Lab Setup](/lab-setup))*
4. Save, then add an **HTTP Method**:
   - **Name:** `getStatus`
   - **HTTP method:** `GET`
   - **Endpoint:** `https://dummyjson.com/carts/${tracking}`
5. Add a **Variable** `tracking` (so the caller supplies the shipment id).
6. Set the **Authentication** (next module — leave it as *No authentication* for now).

You now have a named, reusable integration point. Anyone can call `GlidePort Shipping → getStatus` without knowing the URL.

## Call It From a Script

Server-side code asks for a status and gets a response object:

```js
// A Script Include method that asks the partner where a parcel is
getTrackingStatus: function(trackingNumber) {
    var request = new sn_ws.RESTMessageV2('GlidePort Shipping', 'getStatus');
    request.setStringParameterNoEscape('tracking', trackingNumber);

    var response = request.execute();

    return {
        code: response.getStatusCode(),
        body: response.getBody(),
        error: response.haveError() ? response.getErrorMessage() : null
    };
}
```

Call it from a Business Rule, a Scheduled Job, or a flow's Script step:

```js
var status = new DeliveryUtils().getTrackingStatus(order.getValue('u_tracking_number'));
gs.info('Partner says: ' + status.body);
```

## …Or Build the Request Entirely in Code

When the URL is dynamic or you need a POST with a JSON body, skip the record:

```js
var request = new sn_ws.RESTMessageV2();
request.setEndpoint('https://dummyjson.com/carts/add');
request.setHttpMethod('post');
request.setRequestHeader('Accept', 'application/json');
request.setRequestHeader('Content-Type', 'application/json');
request.setRequestBody(JSON.stringify({
    userId: 1,
    products: [ { id: 1, quantity: 2 } ]   // the parcels to load on this van
}));

var response = request.execute();
```

> **`execute()` is synchronous** — the script waits for the answer. Keep these calls out of `before` Business Rules and off the user's save path; prefer a flow/Scheduled Job so slow partners don't slow the platform.

## The `RESTMessageV2` Cheatsheet

| Method | Purpose |
| --- | --- |
| `setEndpoint(url)` | The full URL to call |
| `setHttpMethod('get' / 'post' / …)` | The verb |
| `setRequestHeader(name, value)` | Add a header (`Content-Type`, API key…) |
| `setStringParameter('name', value)` | Fill a `${name}` in the endpoint (URL-escaped) |
| `setStringParameterNoEscape('name', value)` | Same, without escaping |
| `setRequestBody(jsonString)` | The body for POST/PUT |
| `setBasicAuth(user, pass)` | Basic auth inline (avoid — see Module 2) |
| `execute()` | Send it and get a response |

## Lab: Ask the Partner

1. Create the `GlidePort Shipping → getStatus` REST Message as above, pointed at the sandbox: base `https://dummyjson.com`, method `GET https://dummyjson.com/carts/${tracking}`, with a variable `tracking`.
2. Add a Script Include method `getTrackingStatus(trackingNumber)` using `RESTMessageV2`.
3. Run it from **Scripts Background** with the shipment id `1`.
4. Print the status code and body. Confirm you get a `200` and JSON containing `totalQuantity` (the parcels on that van's manifest).

> **Can't reach it from the instance?** First prove the sandbox works from your own machine with `curl https://dummyjson.com/carts/1` (see [Lab Setup](/lab-setup)). If that works but ServiceNow can't call it, the problem is on the ServiceNow side (endpoint, auth, or MID server) — not the sandbox.

**Check your work:** a reusable named integration point exists, and server-side code can call it and read the response.

## Key Takeaways

- Outbound calls are made with a reusable **REST Message** record or with **`RESTMessageV2`** in code.
- The record hides the URL behind a name; the script form handles dynamic URLs and bodies.
- `execute()` is **synchronous** — keep it off the user's save path.
- The same integration point is callable from scripts, flows, and (next) automations.

## Best Practices

- Name REST Messages after the **partner**, not the technology (`GlidePort Shipping`, not `REST1`).
- Prefer the **declarative record** when a call is reused; it's discoverable by the whole team.
- Always set `Accept`/`Content-Type` explicitly on JSON calls.
- Never inline credentials — Module 2 shows the right way.
