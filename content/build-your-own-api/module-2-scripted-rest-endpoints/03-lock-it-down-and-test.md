# Lock It Down and Test

**Story so far:** The endpoint works — anyone who can reach the instance can read order status. That's fine for a demo and dangerous in production. GlidePort's shipping partners should only read orders they're allowed to, and only registered systems should create orders. Time to lock it down and prove it with real HTTP.

## Step 1 — Who Is Allowed?

Two controls work together:

1. **Authentication** — who is this caller? (User, API key, OAuth token.)
2. **Authorization** — what are they allowed to do? (Roles + ACLs.)

On a Scripted REST resource, set **Requires authentication** and a **Required role**:

- **GET order status** → `Requires authentication` ✔, role: `snc_platform_api` or a custom `u_delivery_partner`.
- **POST create order** → same, role: `u_delivery_partner` (or `admin` only).

Create the role if it doesn't exist: **All → User Administration → Roles → New** → `u_delivery_partner`.

Now a caller without that role gets `403`, and an anonymous caller gets `401`.

## Step 2 — A Secured POST Resource

Add a second resource to the API:

- **Name:** `Create delivery order`
- **Relative path:** `order`
- **HTTP method:** `POST`
- **Requires authentication:** ✔
- **Required role:** `u_delivery_partner`

```js
(function process(request, response) {

    var data = request.body.data;
    if (!data || !data.number) {
        response.setStatus(400);
        response.setBody(JSON.stringify({ error: 'Order number is required' }));
        return;
    }

    var gr = new GlideRecord('u_order_tracking');
    gr.number = data.number;
    gr.setValue('u_priority', data.priority || 'standard');
    gr.setValue('u_urgency', data.urgency || 'low');
    gr.setValue('u_delivery_date', data.delivery_date);
    var sysId = gr.insert();

    response.setStatus(201);
    response.setBody(JSON.stringify({
        sys_id: sysId,
        number: gr.number,
        status: gr.getValue('status')
    }));

})(request, response);
```

### Solid error handling

| Case | Status | Body |
| --- | --- | --- |
| Missing/invalid input | `400` | `{ "error": "..." }` |
| Not authenticated | `401` | (platform handles) |
| Not authorized | `403` | (platform handles) |
| Not found | `404` | `{ "error": "Order not found" }` |
| Unexpected exception | `500` | `{ "error": "Internal error" }` |

Wrap risky logic in `try/catch` and always return a JSON body — never an HTML stack trace.

## Step 3 — Test with Real HTTP

### Basic auth from the terminal

```bash
curl -u "admin:password" \
  "https://<instance>.service-now.com/api/now/delivery/order/ORD0010001"

# POST a new order
curl -u "admin:password" -X POST \
  -H "Content-Type: application/json" \
  -d '{"number":"ORD0010100","priority":"priority","urgency":"high"}' \
  "https://<instance>.service-now.com/api/now/delivery/order"
```

> Use a **test user**, not your admin account, when validating role checks.

### Verify the locks

| Test | Expected |
| --- | --- |
| No credentials | `401` |
| User without `u_delivery_partner` | `403` |
| User with the role | `200` / `201` |
| POST missing `number` | `400` with your JSON error |
| GET unknown order | `404` with your JSON error |

## Step 4 — (Optional) Go OAuth

For production partner integrations, use **OAuth 2.0** instead of basic auth:

1. Create an **OAuth API endpoint** (`All → System OAuth → Application Registry → New`).
2. Choose the client-credentials grant for machine-to-machine calls.
3. Callers trade a client id/secret for an access token, then send `Authorization: Bearer <token>`.

## Best Practices

- Give every resource the **least privilege** role it needs.
- Keep ACLs in the loop — scripted code runs as the caller, but the code you write decides what's returned.
- **Validate everything** in the body; never trust partner input.
- Return consistent JSON errors and correct status codes.
- Version your base path (`delivery/v1`) so partners aren't broken by future changes.

## Key Takeaways

- **AuthN** (who) + **AuthZ** (what) via Requires authentication + Required role + ACLs.
- POST resources read `request.body.data`, validate, insert, and return `201`.
- Map every failure to the right status code and a JSON error body.
- Test with curl and a non-admin user; graduate to OAuth for production.
