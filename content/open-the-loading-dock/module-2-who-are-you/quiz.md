# Quiz: Who Are You?

Answer these questions about authentication and aliases. Your score is saved, and reasoning is revealed after you submit.

1. Why is putting a password directly in a script a bad idea?
   A. It runs slower
   B. The secret leaks into code and update sets, and rotation requires code changes
   C. Scripts can't contain strings
   D. It breaks OAuth
   CORRECT: B
   EXPLAIN: Hardcoded secrets are visible, travel between environments, and must be edited everywhere to rotate.

2. Where should a secret live?
   A. In the script
   B. In a credential record (referenced by name)
   C. In the URL
   D. In a comment
   CORRECT: B
   EXPLAIN: Credentials are stored encrypted and referenced by name, so code never contains the secret.

3. Which OAuth grant fits a server-to-server call with no user involved?
   A. Authorization code
   B. Client credentials
   C. Password
   D. Implicit
   CORRECT: B
   EXPLAIN: Client credentials swaps the client id/secret for a token with no user in the loop — ideal for GlidePort → partner.

4. What does an access token give you that a password doesn't?
   A. Faster calls
   B. It's temporary, scoped, and revocable
   C. It never expires
   D. It removes the need for HTTPS
   CORRECT: B
   EXPLAIN: Tokens expire, carry limited scopes, and can be revoked — far safer than sharing a permanent password.

5. A call fails with 401 in the middle of a long-running integration. Most likely cause?
   A. The record was deleted
   B. The access token expired and needs refreshing
   C. The endpoint URL is wrong
   D. The payload is too large
   CORRECT: B
   EXPLAIN: A mid-run 401 usually means the token expired; refresh it rather than re-checking credentials.

6. What is a Connection & Credential alias?
   A. A copy of a REST Message
   B. A named pointer to connection details and credentials that resolves per environment
   C. A type of flow trigger
   D. An import set
   CORRECT: B
   EXPLAIN: Aliases let code refer to a name; each environment binds it to its own URL and credential.

7. What is the main benefit of aliases over hardcoded URLs and secrets?
   A. They make calls faster
   B. They make integrations portable across environments and rotation a one-place change
   C. They remove the need to authenticate
   D. They store data
   CORRECT: B
   EXPLAIN: Repointing or rotating is a single alias/credential change, with no code edits.

8. Which scope should you request for a read-only shipping integration?
   A. The broadest scope available, to be safe
   B. The narrowest scope that works (e.g. shipping.read)
   C. All scopes on the partner
   D. No scope at all
   CORRECT: B
   EXPLAIN: Least privilege limits the blast radius if a token is ever compromised.
