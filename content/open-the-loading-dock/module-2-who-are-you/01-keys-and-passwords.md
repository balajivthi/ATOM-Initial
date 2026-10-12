# Keys and Passwords

**Story so far:** GlidePort's outbound call works — on a public endpoint. But the van partner won't hand out delivery data to anyone. Every real API wants to know *who* is calling before it answers. This lesson is the family of ways a system proves its identity, and the one rule that matters most: **never bake a secret into code.**

## Why APIs Ask "Who Are You?"

An API that answers anyone is an API that leaks everyone's data. So before it responds, it checks the caller. The check is some form of **authentication** — proving identity — usually followed by **authorization** — proving you're allowed to do *this*.

## The Common Methods

| Method | How it works | GlidePort use |
| --- | --- | --- |
| **Basic auth** | Send `username:password` (base64-encoded) in the `Authorization` header | Simple internal partner APIs |
| **API key** | A long random string in a header or query param | Partner "developer portal" keys |
| **Bearer token** | A token in `Authorization: Bearer <token>` | Most modern APIs, often from OAuth |
| **OAuth 2.0** | Short-lived tokens obtained via a handshake | Anything with user data / scopes (next lesson) |
| **mTLS** | Mutual client certificates | High-security / on-prem partners |

Basic auth over HTTPS is fine; over plain HTTP it's a password in clear text — never do that.

## Setting Auth on a Call

```js
var request = new sn_ws.RESTMessageV2('GlidePort Shipping', 'getStatus');
request.setBasicAuth('glideport_api', 'S3cr3t!');   // ← WORKS, but don't do this
request.setRequestHeader('X-Api-Key', 'abc123');     // ← also works, also don't
```

Both *work*. Both are **wrong** in real code, because:

- The secret is now **in the script**, visible to anyone who can read it.
- It's copied into **update sets** and moves between environments.
- Rotating the password means **editing code and redeploying**.
- Dev and prod secrets get tangled together.

## The Right Home for a Secret

Secrets belong in a **credential record**, referenced by name — never typed into a script:

1. **All → Connections & Credentials → Credentials → New**.
2. **Name:** `GlidePort Shipping – API`
3. Choose the type (**Basic Auth Credentials**), enter the username and password.
4. Save. The password is now stored **encrypted**, and the record can be restricted.

Then reference it from the REST Message's **Authentication** tab, or from an **alias** (next lesson). The calling code never sees the secret.

```
Script  ──calls──▶  REST Message "GlidePort Shipping"
                          │  uses
                          ▼
                    Credential: "GlidePort Shipping – API"   ← secret lives here, encrypted
```

## What to Put in a Credential vs a Header

| Belongs in a credential | Belongs in code/request |
| --- | --- |
| Username & password | The endpoint URL |
| API key / client secret | `Content-Type`, `Accept` |
| OAuth client id & secret | The request body |
| Certificates / tokens | Business data (order number…) |

## Rotating Without Code Changes

The payoff shows up on rotation day. The partner forces a new API key:

- **Hardcoded:** find every script, edit, retest, redeploy. Miss one → production breaks.
- **Credential record:** update the one credential. Every caller picks it up immediately.

That's the whole argument in one example.

## Lab: Move the Secret Out of the Script

1. Create a Credential named `GlidePort Shipping – API` with a dummy username/password.
2. On your `GlidePort Shipping` REST Message, open the HTTP Method's **Authentication** tab and select that credential.
3. Delete any `setBasicAuth(...)` line from your Script Include.
4. Call it again and confirm it still authenticates (use a sandbox that echoes your auth, or just confirm no error).
5. Change the credential's password and confirm the caller uses the new value with **zero code changes**.

**Check your work:** no secret appears in any script; the credential record is the single source of truth.

## Key Takeaways

- APIs authenticate the caller: **Basic, API key, Bearer token, OAuth, mTLS**.
- `setBasicAuth`/inline keys **work but are wrong** — they leak secrets into code and update sets.
- Secrets live in **credential records**, stored encrypted and referenced by name.
- **Rotation** is the test: credentials change in one place; hardcoded secrets change everywhere.
- Keep only non-secret values (`URL`, headers, body) in code.

## Best Practices

- One credential per **partner and environment**; name them clearly.
- Never paste a real secret into a script, a wiki, or a chat — put it in the credential store.
- Restrict who can read credential records.
- Assume any secret that ever touched code is compromised — rotate it.
