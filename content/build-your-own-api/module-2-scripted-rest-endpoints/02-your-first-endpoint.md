# Your First Endpoint

**Story so far:** The API design is on paper — partners should be able to `GET /delivery/order/{order_number}` and see a delivery's status. Now we build it for real: a Scripted REST API, a resource, and a method with working server-side code.

## Step 1 — Create the Scripted REST API

1. **All → System Web Services → Scripted REST APIs → New**.
2. **Name:** `GlidePort Delivery API`
3. **API ID:** `glideport-delivery` (this forms the URL segment)
4. **API root path:** `delivery` (leave it as-is or use a versioned root like `delivery/v1`)
5. Leave the default base path `api/now` selected, or set a custom base path if your instance allows.

The resulting base URL is:

```text
https://<instance>.service-now.com/api/now/delivery
```

## Step 2 — Add a Resource

1. Under the API, open the **Resources** related list and click **New**.
2. **Name:** `Order status`
3. **Relative path:** `order/{order_number}` — the `{...}` is a **path parameter**.
4. **HTTP method:** `GET`
5. **Requires authentication:** ✔ (checked)

## Step 3 — Write the Method Script

Paste this into the **Script** field:

```js
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

    var orderNumber = request.pathParams.order_number;
    var gr = new GlideRecord('u_order_tracking');

    if (!gr.get('number', orderNumber)) {
        response.setStatus(404);
        response.setBody(JSON.stringify({ error: 'Order not found' }));
        return;
    }

    response.setStatus(200);
    response.setBody(JSON.stringify({
        number: gr.getValue('number'),
        status: gr.getValue('status'),
        priority: gr.getValue('u_priority'),
        urgency: gr.getValue('u_urgency'),
        agent: gr.getValue('u_agent'),
        delivery_date: gr.getValue('u_delivery_date')
    }));

})(request, response);
```

### The request object

| Object | Gives you |
| --- | --- |
| `request.pathParams.order_number` | Path params (`{order_number}`) |
| `request.queryParams.status` | Query params (`?status=shipped`) |
| `request.body.data` | Parsed JSON body (for POST/PUT) |
| `request.headers` | Request headers |

### The response object

| Call | What it does |
| --- | --- |
| `response.setStatus(200)` | Sets the HTTP status code |
| `response.setBody(jsonString)` | Sets the response body |
| `response.setHeader('name', 'value')` | Sets a header |
| `response.getStreamWriter()` | Streams a large response |

## Step 4 — Test It (REST API Explorer)

The fastest in-app test:

1. **All → System Web Services → REST API Explorer**.
2. Find the GlidePort Delivery API → the `Order status` resource.
3. Enter an order number as the path param and click **Send**.
4. Expect a `200` with your JSON.

If your instance has no orders yet, create one first (or POST one — see the next lesson).

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| `gr.get('number', ...)` fails | Use the exact field name and value format; `number` is a system field |
| 401 on test | Check **Requires authentication** is on and you're logged in / passing credentials |
| JSON body not shown | Use `JSON.stringify(...)` — `setBody` takes a **string** |
| Path param undefined | The `{order_number}` in the resource path must match `request.pathParams.order_number` |

## Key Takeaways

- Scripted REST API = base URL; **Resources** = paths; **Methods** = HTTP verbs with scripts.
- `{param}` in the path becomes `request.pathParams.param`.
- `request` gives input; `response.setStatus` + `response.setBody` give output.
- Test in REST API Explorer before involving external clients.
