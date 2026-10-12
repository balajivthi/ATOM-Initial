# Quiz: The Outbound Desk

Answer these questions about outbound integrations. Your score is saved, and reasoning is revealed after you submit.

1. What is the difference between outbound and inbound integration?
   A. Outbound is faster
   B. Outbound means GlidePort calls the other system; inbound means the other system calls GlidePort
   C. Inbound is only for files
   D. There is no difference
   CORRECT: B
   EXPLAIN: Direction is the whole distinction: outbound = we call them, inbound = they call us.

2. Which object makes an outbound REST call from server-side script?
   A. GlideRecord
   B. sn_ws.RESTMessageV2
   C. GlideAjax
   D. AbstractAjaxProcessor
   CORRECT: B
   EXPLAIN: RESTMessageV2 (sn_ws.RESTMessageV2) builds and executes outbound HTTP requests.

3. What does `execute()` do?
   A. Queues the call to run later
   B. Sends the request synchronously and returns the response
   C. Deletes the REST Message record
   D. Parses JSON automatically
   CORRECT: B
   EXPLAIN: execute() sends the request and blocks until a response comes back — so keep it off the user's save path.

4. `response.haveError()` returns true. What does that mean?
   A. The partner returned a 404
   B. The HTTP call itself failed (transport/connection error)
   C. The JSON had a missing field
   D. The response body is empty
   CORRECT: B
   EXPLAIN: haveError() flags a failed call; a 404 is a successful round-trip with a negative answer and is not a haveError() case.

5. Which status codes usually justify an automatic retry?
   A. 400 and 404
   B. 429 and 5xx
   C. 200 and 201
   D. 401 and 403
   CORRECT: B
   EXPLAIN: 429 (rate-limited) and 5xx (server error) are typically transient; 400/404 are permanent and retrying won't help.

6. `getBody()` returns what?
   A. A parsed JavaScript object
   B. A string (usually JSON) that you must parse
   C. A GlideRecord
   D. The HTTP status code
   CORRECT: B
   EXPLAIN: getBody() returns raw text; use JSON.parse (with a guard) to turn it into data.

7. Why send an Idempotency-Key header on a call that creates or changes something?
   A. To make the call faster
   B. So a retry is recognised as the same operation and doesn't duplicate the effect
   C. To authenticate the request
   D. To change the HTTP method
   CORRECT: B
   EXPLAIN: An idempotency key lets the partner dedupe repeats, so a retried write happens only once.

8. Where can you review the outbound calls your instance has made?
   A. The system dictionary
   B. The Outbound HTTP Requests log (sys_outbound_http_log)
   C. The client script editor
   D. The transform map
   CORRECT: B
   EXPLAIN: Outbound HTTP requests are recorded for inspection, which is essential for debugging integrations.
