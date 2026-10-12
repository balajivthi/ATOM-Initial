# REST in 15 Minutes

**Story so far:** GlidePort's customers want to check delivery status from their own systems, and external shipping partners want to push tracking events in. The Service Portal is for humans; the platform needs a **language for machines** — that's REST.

## What Is REST?

**REST** (Representational State Transfer) is a style of API where clients talk to a server over HTTP using **URLs** (resources) and **HTTP methods** (actions).

A request is made up of:

| Piece | Example |
| --- | --- |
| **URL** | `https://<instance>.service-now.com/api/glideport/delivery/ORD0010001` |
| **Method** | `GET` (read), `POST` (create), `PUT`/`PATCH` (update), `DELETE` (remove) |
| **Headers** | `Authorization`, `Content-Type: application/json` |
| **Body** (some methods) | JSON data |

The server replies with a **status code** and often a JSON body:

| Code | Meaning |
| --- | --- |
| `200` / `201` | OK / Created |
| `400` | Bad request (your input was wrong) |
| `401` / `403` | Not authenticated / not authorized |
| `404` | Not found |
| `500` | Server error |

## Paths, Query Params, and Body

- **Path params** identify a specific resource: `/order/ORD0010001` → the order number.
- **Query params** filter or tune: `/order?status=shipped&limit=10`.
- **Body** carries data for create/update: `{ "status": "shipped" }`.

```text
GET /api/glideport/delivery/ORD0010001
→ 200 {"number":"ORD0010001","status":"shipped","agent":"Ana"}

GET /api/glideport/delivery?status=shipped
→ 200 [{"number":"ORD0010002","status":"shipped"}, ...]

POST /api/glideport/delivery
Body: {"number":"ORD0010009","status":"new","agent":"Bo"}
→ 201 {"number":"ORD0010009","status":"new","agent":"Bo"}
```

## Why Scripted REST APIs on the Platform?

ServiceNow ships tons of out-of-the-box REST APIs (Table API, Import Set API, etc.). You write a **Scripted REST API** when you need a **custom endpoint**: a tailored payload, a domain-specific resource (`/delivery/order/status`), or logic that shouldn't be a raw table write.

A Scripted REST API is a **URL**, plus **Resources** (paths under it), each with **methods** (GET/POST/…) backed by server-side scripts.

## Your First GlidePort URL

Let's design the Delivery API the partners will use:

| Resource | Method | Purpose |
| --- | --- | --- |
| `/delivery/order/{order_number}` | GET | Check status of one order |
| `/delivery/order` | GET | List orders, optionally filtered |
| `/delivery/order` | POST | Register a new delivery order |

Everything else you already know applies: the script inside is plain platform scripting — GlideRecord + GlideSystem.

## Best Practices for API Design

- Use **nouns, not verbs** in URLs: `/order/{id}`, not `/getOrder`.
- Return **meaningful status codes** and consistent JSON shapes.
- **Version** the API (e.g. `/api/glideport/delivery/v1/...`) so changes don't break partners.
- Keep responses minimal — return what the client needs, never raw table dumps.
- Always **authenticate and authorize** (next lessons).

## Key Takeaways

- REST = URLs + HTTP methods + JSON; status codes tell you what happened.
- Path params pick a resource; query params filter; the body carries data.
- Scripted REST APIs give you custom endpoints with full server-side logic.
- Design nouns-first, versioned, consistent, and secured.
