# Quiz: The Inbound Dock

Answer these questions about inbound and batch integrations. Your score is saved, and reasoning is revealed after you submit.

1. Why should an inbound event handler respond quickly rather than process the work inline?
   A. Because JSON is slow
   B. The partner's system is waiting; heavy work should be decoupled and processed asynchronously
   C. To avoid authentication
   D. Because staging tables can't be written to
   CORRECT: B
   EXPLAIN: Authenticate, validate, store, and return 202; let a flow/job do the heavy lifting so the caller isn't blocked.

2. What status code commonly means "received, will process later"?
   A. 200 OK
   B. 202 Accepted
   C. 404 Not Found
   D. 500 Server Error
   CORRECT: B
   EXPLAIN: 202 Accepted is the standard "I got it, processing asynchronously" acknowledgement.

3. Why must an inbound endpoint authenticate the caller?
   A. To make it faster
   B. An open endpoint lets anyone inject data; the URL being unknown is not security
   C. Because JSON requires it
   D. To avoid using staging tables
   CORRECT: B
   EXPLAIN: URLs leak; without authentication any client can post data — reject unknown callers with 401.

4. A partner retries and sends the same event twice. What prevents a duplicate?
   A. Returning 202
   B. De-duplicating on a correlation/event id before processing
   C. Using HTTPS
   D. Coalescing the URL
   CORRECT: B
   EXPLAIN: Idempotency via an event id ensures each distinct event is processed exactly once.

5. In the Import Set pipeline, what is the role of the staging (import set) table?
   A. It is the final target table
   B. It holds raw rows in isolation so bad data doesn't touch real records until a transform succeeds
   C. It authenticates the partner
   D. It replaces the transform map
   CORRECT: B
   EXPLAIN: Staging isolates raw data, is auditable and re-runnable, and protects target records.

6. What does setting "coalesce" on the tracking field do?
   A. Deletes duplicate rows
   B. Matches an existing target record and updates it; otherwise inserts a new one
   C. Encrypts the field
   D. Authenticates the import
   CORRECT: B
   EXPLAIN: Coalesce turns a load into an upsert, so re-running a file doesn't create duplicates.

7. Why is a Data Stream / Stream Connect different from a nightly file import?
   A. It runs once a day
   B. It keeps records in sync near-continuously from a change feed
   C. It only handles CSV
   D. It can't use coalesce
   CORRECT: B
   EXPLAIN: Streams apply changes continuously, like an import set that never stops running.

8. What is a "watermark" used for in a scheduled REST pull?
   A. Encrypting the payload
   B. Remembering the last successful sync point so each run fetches only what changed
   C. Styling the response
   D. Authenticating the request
   CORRECT: B
   EXPLAIN: A watermark (last good timestamp/offset) prevents re-fetching everything and keeps sync gap-free.
