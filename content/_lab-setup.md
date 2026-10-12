# Lab Setup & Practice Ground

Every lab in this portal runs against something **real**: a free ServiceNow Personal Developer Instance (PDI) for the platform work, and, for the integration course, a set of **free, public, no-install sandbox APIs**. Nothing here is a made-up URL you have to imagine — you can run every call below from a terminal *before* you wire it into ServiceNow.

Set this up once. Every course reuses it.

## Part 1 — Get a Personal Developer Instance (PDI)

Most courses build things *inside* ServiceNow, so you need your own free instance.

1. Go to [developer.servicenow.com](https://developer.servicenow.com) and create a free account.
2. Click **Request an Instance** and pick the latest release.
3. Save three things: the **instance URL** (`https://dev#######.service-now.com`), the **admin username**, and the **password**.

Everything that is "on the platform" — tables, forms, GlideRecord, Business Rules, Client Scripts, Flow Designer, Scripted REST, Import Sets, Virtual Agent — happens on this instance.

## Part 2 — The GlidePort Partner Sandbox

The integration course (*Open the Loading Dock*) needs to talk to systems **outside** ServiceNow. A real company won't hand live access to a stranger, and a made-up `api.partner.example` teaches you nothing because it never answers. So we use free public **practice APIs** that behave like a partner's systems.

When you connect to a real partner, only the **base URL** and the **credentials** change — the work is identical. That is the whole point.

You sign up for **nothing** below. They are open to everyone.

| Sandbox | Base URL | Stands in for | What it does |
| --- | --- | --- | --- |
| **Van partner** | `https://dummyjson.com` | The van partner's shipping API | Returns a manifest (`/carts/{id}`), books a load (`POST /carts/add`), lists delivery agents (`/users`) |
| **Request & auth** | `https://httpbin.org` | Any partner's auth and protocol layer | Verifies Basic/Bearer auth, echoes what you sent, and returns any status code on demand |
| **OAuth server** | `https://demo.duendesoftware.com` | A partner's OAuth 2.0 token issuer | Issues **real** client-credentials tokens |
| **Live feed** | `https://api.open-meteo.com` | A live "van telemetry" feed | Returns current conditions that change on every call |

### Van partner sandbox — the calls you'll use

| Call | Method | You get back |
| --- | --- | --- |
| `/carts/1` | GET | A "shipment manifest": `{ "id": 1, "userId": 1, "total": 13037.88, "totalQuantity": 12, "products": [ … ] }` |
| `/carts/99999` | GET | **404** — an unknown shipment (perfect for error-handling labs) |
| `/carts/add` | POST | **201** and the created cart, with a new `id` — your "booking id" |
| `/users/1` | GET | A delivery agent: `{ "id": 1, "firstName": "Emily", "lastName": "Johnson", "email": "…" }` |
| `/users?limit=5` | GET | `{ "users": [ … ], "total": 100, "skip": 0, "limit": 5 }` |

Try it now:

```bash
curl https://dummyjson.com/carts/1
curl -i https://dummyjson.com/carts/99999          # -> HTTP/1.1 404
curl -X POST https://dummyjson.com/carts/add \
  -H "Content-Type: application/json" \
  -d '{"userId":1,"products":[{"id":1,"quantity":2}]}'   # -> 201, new id
```

### Request & auth sandbox — the calls you'll use

| Call | Method | You get back |
| --- | --- | --- |
| `/basic-auth/glideport/S3cr3t` | GET | **401** without Basic auth, **200** with the matching username/password |
| `/bearer` | GET | **200** only when you send `Authorization: Bearer <anything>` |
| `/headers` | GET | The headers *you* sent — proof your auth/headers left the building |
| `/anything` | POST | Echoes your method, headers, body — a mirror for any request |
| `/status/404`, `/status/429`, `/status/500` | GET | Returns exactly that status code, on demand |

Try it now:

```bash
curl -i https://httpbin.org/basic-auth/glideport/S3cr3t                     # -> 401
curl -i -u glideport:S3cr3t https://httpbin.org/basic-auth/glideport/S3cr3t # -> 200
curl -i https://httpbin.org/status/500                                       # -> 500
curl -i -H "Authorization: Bearer faketoken" https://httpbin.org/bearer      # -> 200
```

### OAuth server — a real handshake

The public demo IdentityServer issues real tokens. These credentials are **not secrets** — they are published by the vendor for demos:

| Setting | Value |
| --- | --- |
| Token URL | `https://demo.duendesoftware.com/connect/token` |
| Grant type | `client_credentials` |
| Client ID | `m2m` |
| Client secret | `secret` |
| Scope | `api` |
| Protected resource | `https://demo.duendesoftware.com/api/test` |

Try the *whole* handshake from a terminal:

```bash
# 1. swap the client id/secret for a real access token
curl -s https://demo.duendesoftware.com/connect/token \
  -d grant_type=client_credentials -d client_id=m2m -d client_secret=secret -d scope=api

# 2. use the token (copy access_token from step 1)
curl -i -H "Authorization: Bearer <access_token>" https://demo.duendesoftware.com/api/test
#   -> 200 with a token; 401 without one
```

### Live feed — genuinely changing data

Open-Meteo needs no key and returns conditions that change every minute, so it proves your integration is pulling *fresh* data:

```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=-0.13&current=temperature_2m,wind_speed_10m"
#   -> { "current": { "time": "2026-10-12T05:45", "temperature_2m": 14.2, "wind_speed_10m": 9.4 }, … }
```

## Part 3 — Testing inbound calls (the partner calls *you*)

Some labs have the partner **push** to your instance. That means *you* play the partner and send an HTTP call to **your own PDI** (it is reachable on the public internet).

**Option A — a test client (simplest).** From a terminal, Postman, or the free browser tool [Hoppscotch](https://hoppscotch.io), send a request like:

```bash
curl -i -X POST "https://YOUR-INSTANCE.service-now.com/api/now/van/events" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: the-key-you-configured" \
  -d '{"event":"delivered","event_id":"evt-001","tracking":"1","at":"2026-10-12T14:02:00Z"}'
```

**Option B — a second PDI (the "two instances" trick).** Request a second free developer instance and call the first one's Scripted REST endpoint from a Script Include / REST Message there. This exercises the real outbound→inbound path with no external tool at all. Ideal for the capstone.

Either way, you are simulating what the partner's system would do.

## Part 4 — Keeping it honest

- **These are third-party services.** They are stable and widely used, but they are not ours. If one is ever unreachable, `httpbingo.org` is a drop-in mirror of `httpbin.org`, and `jsonplaceholder.typicode.com` is a simpler CRUD sandbox. The lessons name the exact call they use, so swapping the base URL is a one-line change.
- **Treat sandbox secrets as fake.** The OAuth client id/secret above are public demo values. Real partner credentials go in a **credential record / alias** — never in code (you'll learn exactly how in Module 2).
- **Every endpoint here is HTTP(S) and reachable from a cloud PDI.** If a call works from your laptop's `curl` but not from ServiceNow, the problem is on the ServiceNow side (auth, alias, MID server), not the sandbox.
