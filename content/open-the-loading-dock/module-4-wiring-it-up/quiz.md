# Quiz: Wiring It Up

Answer these questions about prebuilt integrations, monitoring, and design. Your score is saved, and reasoning is revealed after you submit.

1. What is a "spoke" in the platform's integration engine?
   A. A hand-written REST call
   B. A prebuilt set of actions for one external system (e.g. Teams, Jira)
   C. A database table
   D. A type of credential
   CORRECT: B
   EXPLAIN: Spokes provide vendor-managed actions you can drag into a flow, with details handled for you.

2. When should you prefer a spoke action over a hand-written script?
   A. Never
   B. When a prebuilt spoke exists for that system and fits the job
   C. Only for outbound calls
   D. Only when there is no authentication
   CORRECT: B
   EXPLAIN: Reach for the simplest fit — a spoke avoids re-implementing a common integration.

3. Which of these requires an IntegrationHub entitlement?
   A. Scheduled jobs
   B. Spoke actions
   C. Outbound REST via RESTMessageV2
   D. Import sets
   CORRECT: B
   EXPLAIN: Spokes are licensed; the base platform still covers REST, scheduled jobs, and import sets.

4. Where would you look to confirm an outbound partner call actually happened?
   A. The system dictionary
   B. The Outbound HTTP Requests log (sys_outbound_http_log)
   C. The transform map
   D. The client script editor
   CORRECT: B
   EXPLAIN: Outbound HTTP requests are logged with URL, method, status, and body — the first stop for debugging.

5. A call returns 429. What is the correct response?
   A. Retry immediately in a tight loop
   B. Back off (honor Retry-After) and retry, capped
   C. Delete the record
   D. Treat it as permanent and never retry
   CORRECT: B
   EXPLAIN: 429 is a rate limit — transient, so back off and retry, but not forever.

6. Which failure should NOT be retried automatically?
   A. 500 server error
   B. 429 rate limited
   C. 400 bad request
   D. A connection timeout
   CORRECT: C
   EXPLAIN: 400 means your payload is wrong — retrying won't help; log and fix it.

7. Why is a silent Catch block dangerous in an integration?
   A. It uses too much memory
   B. The integration appears to work while the real work never happens
   C. It disables logging globally
   D. It changes the HTTP method
   CORRECT: B
   EXPLAIN: Swallowing errors hides failures; a Catch should log, alert, and/or recover.

8. Which combination best makes retries and re-runs safe?
   A. HTTPS and JSON
   B. Idempotency keys on writes and coalesce on imports
   C. Spokes and stages
   D. Polling and pagination
   CORRECT: B
   EXPLAIN: Idempotency (outbound/inbound) and coalesce (imports) ensure repeated operations don't duplicate effects.

9. What is the main benefit of authenticating outbound integrations with an alias?
   A. Faster calls
   B. Portable across environments and rotatable without code changes
   C. It removes the need for OAuth
   D. It stores business data
   CORRECT: B
   EXPLAIN: A named alias binds connection + credential per environment, so code stays clean and portable.

10. A nightly import reports "rows loaded, none transformed." First thing to check?
   A. The partner's website
   B. The transform map's condition / coalesce settings
   C. The user's browser
   D. The flow trigger
   CORRECT: B
   EXPLAIN: Rows landing but not transforming points at the transform map (mapping, conditions, coalesce).
