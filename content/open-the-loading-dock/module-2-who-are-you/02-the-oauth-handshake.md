# The OAuth Handshake

**Story so far:** Basic auth and API keys are fine for a simple internal partner — but the van partner (and everyone else modern) wants something better: short-lived **tokens** that expire, get scoped, and can be revoked. That's **OAuth 2.0**, and it starts with a handshake.

## The Problem OAuth Solves

Handing a partner your password is forever-access. If it leaks, you're exposed until someone changes it, everywhere. OAuth replaces "here's my password" with:

> "Here's a **token** that expires in an hour and only lets me read shipping status."

A token is **temporary**, **scoped**, and **revocable**. That's why nearly every serious API uses it.

## The Cast of Characters

| Actor | Role |
| --- | --- |
| **Client** | GlidePort (the caller) |
| **Authorization server** | The partner's token issuer (`/oauth/token`) |
| **Resource server** | The API that holds the data |
| **Client ID / secret** | GlidePort's identity, issued by the partner |
| **Access token** | The short-lived key you send with each call |
| **Refresh token** | A longer-lived key to get new access tokens |
| **Scope** | What the token is allowed to do (e.g. `shipping.read`) |

## The Handshake (Client Credentials)

For **server-to-server** calls — no human clicking "Allow" — the **client credentials** grant is the fit. GlidePort swaps its client id/secret for a token:

```
POST https://auth.shipping.example/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=glideport-client
&client_secret=••••••
&scope=shipping.read shipping.write
```

The server replies:

```json
{
  "access_token": "eyJhbGciOi...", 
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "shipping.read shipping.write"
}
```

Then every API call carries the token:

```
GET https://api.shipping.example/v1/track/GP123
Authorization: Bearer eyJhbGciOi...
```

When the token expires, you either request a new one or use the **refresh token** to get one without re-sending the client secret.

## The Grant Types

| Grant | Who's involved | Use for |
| --- | --- | --- |
| **Client credentials** | Machine → machine | Server-to-server, no user |
| **Authorization code** | A user consents in a browser | Acting on behalf of a user |
| **Password** (legacy) | User gives username/password | Older first-party APIs |
| **JWT bearer** | A signed assertion | Advanced / federated setups |

GlidePort calling the van partner with no user involved → **client credentials**.

## Doing It in GlidePort

You don't hand-craft the handshake. Register the partner as an **OAuth provider** and let the platform manage tokens:

1. **All → System OAuth → Application Registry → New → Connect to a third party OAuth Provider**.
2. Enter the partner's details: **Client ID**, **Client Secret**, **Authorization/Tolken URLs**, the **grant type**, and the **scopes**.
3. **Save** and **Get OAuth Token** to confirm the handshake works.
4. Reference the provider from your integration — via the REST Message's authentication, or `request.setAuthenticationProfile('oauth2', <providerOrAlias>)`.

The platform **caches** the access token and **refreshes** it for you. Your script just calls the API:

```js
var request = new sn_ws.RESTMessageV2('GlidePort Shipping', 'getStatus');
// Authentication is configured on the REST Message method (OAuth provider / alias)
request.setStringParameterNoEscape('tracking', trackingNumber);
var response = request.execute();
```

## Token Handling Rules

- **Never** log or store an access token yourself — treat it like a password.
- Store the **client secret** in a credential/alias, not in the OAuth record's plain fields if you can avoid it.
- Expect **expiry**: a `401` mid-integration usually means "get a fresh token," not "bad credentials."
- Request the **narrowest scope** you need (`shipping.read`, not `admin`).
- If a refresh fails repeatedly, alert — tokens can be revoked.

## Lab: Walk the Handshake

1. Register a dummy **third-party OAuth provider** in Application Registry using `client_credentials`.
2. Point it at a test OAuth server (or a sandbox partner). Enter a client id/secret.
3. Click **Get OAuth Token** and confirm you receive an access token.
4. Configure your `GlidePort Shipping → getStatus` method to use this provider.
5. Call it and confirm the request goes out with a `Bearer` token (check the Outbound HTTP log).

**Check your work:** the token is obtained and cached by the platform, and the API call authenticates without any secret appearing in your script.

## Key Takeaways

- OAuth trades a permanent password for a **short-lived, scoped, revocable token**.
- **Client credentials** is the grant for server-to-server integrations like GlidePort → van partner.
- The handshake: send client id/secret → receive an access token → send it as `Authorization: Bearer`.
- Register the provider once; the **platform caches and refreshes** tokens for you.
- Treat tokens as secrets and request the **narrowest scope** that works.

## Best Practices

- Prefer **client credentials** when no user is involved; use **authorization code** only when acting as a user.
- Keep the **client secret in a credential/alias**, never in plain text or code.
- Handle `401` as "refresh the token," and alert if refreshes keep failing.
- Record which **scopes** you requested and why — least privilege.
