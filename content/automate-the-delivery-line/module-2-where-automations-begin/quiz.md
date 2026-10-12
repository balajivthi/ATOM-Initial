# Quiz: Where Automations Begin

Answer these questions about triggers, conditions, and run modes. Your score is saved, and reasoning is revealed after you submit.

1. Which trigger fires on a clock rather than a record change?
   A. Record → Created
   B. Scheduled
   C. Inbound Email
   D. Service Catalog
   CORRECT: B
   EXPLAIN: A scheduled trigger starts the flow on a schedule; it provides no current record, so you look records up inside the flow.

2. An "on update" flow fires for every field edit. What is the cleanest fix?
   A. Add a Business Rule to block updates
   B. Watch the specific field with the "changes" condition on the trigger
   C. Convert the flow to a scheduled job
   D. Ask users to stop editing records
   CORRECT: B
   EXPLAIN: A field-watch with the "changes" operator makes the trigger fire only when the field you care about actually moves.

3. What does the trigger condition "Status changes" guarantee?
   A. The flow runs on every save
   B. The flow runs only on the update where Status actually changes value
   C. Status can never be edited
   D. The flow runs once per day
   CORRECT: B
   EXPLAIN: "changes" is edge-aware: it is true only when the field's value differs from its previous value.

4. A scheduled trigger provides no current record. How do you get the records to work on?
   A. They arrive automatically as data pills
   B. With a Look Up Records action (usually fanned out with For Each)
   C. You cannot; scheduled flows can't touch records
   D. From the notification template
   CORRECT: B
   EXPLAIN: Scheduled flows fetch their own data with Look Up Records, then loop over the results.

5. An escalation flow creates a duplicate task on every save. Which run mode fixes this most cheaply?
   A. For each update
   B. Once, or "Only if condition was false and becomes true"
   C. A wider trigger condition
   D. A Try/Catch block
   CORRECT: B
   EXPLAIN: Once (or edge/true-flip) firing prevents the re-run at the source, without adding guards inside the flow.

6. What does the flow's "run as" user control?
   A. The font used in notifications
   B. The permissions the flow's reads and writes are performed with
   C. How fast the flow executes
   D. The flow's trigger table
   CORRECT: B
   EXPLAIN: Run-as determines the access level of every action; system/service accounts get broad access, a user gets only that user's access.

7. Flows run asynchronously. What does that mean for the user?
   A. The user's save waits until the flow finishes
   B. The user's save completes immediately and the flow proceeds in the background
   C. The flow only runs at night
   D. The flow cannot read the record
   CORRECT: B
   EXPLAIN: Async execution keeps the UI responsive and runs the flow after the save — which is why run modes matter for overlapping updates.

8. For "create the van task exactly once per order," which run mode fits best?
   A. For each update
   B. For each unique change
   C. Once
   D. Run on a schedule
   CORRECT: C
   EXPLAIN: Once guarantees the work happens at most a single time per record, no matter how many later updates occur.
