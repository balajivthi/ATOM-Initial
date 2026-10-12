# Aliases, Not Hardcoded Secrets

**Story so far:** You can authenticate with Basic, keys, or OAuth. Now the organisational problem: GlidePort has *four* environments (dev, test, staging, prod) and each partner has *different* URLs and credentials for each. Pasting those into every REST Message is how integration rot begins. The fix is the **alias**.

## The Environment Sprawl Problem

Without aliases, every integration points at a hardcoded URL and a hardcoded credential:

```
Dev  REST Message → https://dummyjson.com                 + dev credential
Prod REST Message → https://jsonplaceholder.typicode.com  + prod credential
```

> Two live sandboxes stand in for dev and prod here so you can *watch* a call follow its alias (see [Lab Setup](/lab-setup)). In a real shop these would be the partner's sandbox and live hosts.

Multiply by every partner × every method × every environment, and you have a maintenance nightmare. Change the prod URL and you're editing dozens of records.

## What an Alias Is

A **Connection & Credential alias** is a *named pointer* to connection details and credentials that can **resolve differently per environment**:

```
Code:  request.setAuthenticationProfile('basic', 'shipping-api')
                                   │
                                   ▼
     Alias "shipping-api"
       dev  → sandbox URL + dev credential
       prod → live URL    + prod credential
```

Your code says *"shipping-api"* — it never knows the URL or secret. Each environment supplies its own.

## The Three Alias Types

| Type | Holds | Use for |
| --- | --- | --- |
| **Connection** | A base URL / host | Endpoint targets |
| **Credential** | A secret (user/pass, token, key) | Authentication |
| **Connection & Credential** | Both together | The usual choice for integrations |

## Where Aliases Live

- **Create:** build the underlying **Connection** and **Credentials** records, then the alias that combines them — under **All → Connections & Credentials**.
- **Referenced by name** from REST Messages, OAuth provider records, flow REST steps, and scripts.

Using one in a script:

```js
var request = new sn_ws.RESTMessageV2();
request.setEndpoint('https://dummyjson.com/carts/' + tracking);
request.setHttpMethod('get');
request.setAuthenticationProfile('basic', 'shipping-api');   // alias name/id
var response = request.execute();
```

Switching environments never touches this code — only the alias's binding does.

## Why This Is The Whole Point

| Without aliases | With aliases |
| --- | --- |
| URL + secret in every record | One named alias per partner |
| Update N records to change a URL | Update one alias |
| Secrets scattered in code/update sets | Secrets in credentials; code is clean |
| Dev/prod mix-ups | Environment binds the right values |
| New environment = rebuild integrations | New environment = rebind aliases |

## Hardcoding vs Credential vs Alias

| Approach | Secret safe? | Environment-portable? | Recommended? |
| --- | --- | --- | --- |
| `setBasicAuth(user, pass)` in code | ❌ | ❌ | Never |
| Plain **Credential** record referenced directly | ✅ | ⚠️ needs care | Sometimes |
| **Connection & Credential alias** | ✅ | ✅ | ✅ Preferred |

A plain credential protects the secret; an alias protects the secret *and* makes the integration portable across environments.

## Lab: Alias the Partner

1. Create a **Connection** `Shipping API – Connection` with the base URL `https://dummyjson.com`.
2. Create **Credentials** `Shipping API – Credential` with a dummy user/pass.
3. Create a **Connection & Credential alias** named `shipping-api` combining the two.
4. Update your outbound call to use `setAuthenticationProfile('basic', 'shipping-api')`.
5. Simulate an environment switch: repoint the connection's URL to `https://jsonplaceholder.typicode.com` and call again — confirm the call now goes to the *new* host with **no code change** (check the Outbound HTTP log).

**Check your work:** the integration references one alias by name; no URL or secret is hardcoded, and repointing the alias changes where the call goes.

## Key Takeaways

- **Aliases** (Connection & Credential) give integrations a **name** instead of a URL + secret.
- They resolve **per environment**, so the same code works in dev/test/prod.
- Use them to **rotate** credentials and **repoint** endpoints without editing code.
- Prefer **Connection & Credential** aliases for typical integrations.
- Combined with credentials (previous lessons), code contains **zero secrets**.

## Best Practices

- One alias per **partner + capability** (`shipping-api`, `payments-api`).
- Name aliases after the **business service**, not the transport.
- Keep the underlying connection/credential records restricted.
- Document which alias an integration expects — it's part of its contract.
