# Quiz: The Assembly Line

Answer these questions about flow foundations. Your score is saved, and reasoning is revealed after you submit.

1. What is the best signal that you should reach for a flow instead of a Business Rule?
   A. The work reacts to a single field change on one record
   B. The work spans several steps, tables, or days
   C. The work must run inside a form's browser session
   D. The work only needs to log a message
   CORRECT: B
   EXPLAIN: Multi-step journeys across tables and time are exactly what Flow Designer is built for; a single reflexive change is leaner as a Business Rule.

2. Which block can appear first on a flow canvas?
   A. An action
   B. A flow logic block
   C. A trigger
   D. A flow variable
   CORRECT: C
   EXPLAIN: Every flow begins with exactly one trigger, which also supplies the record (and its data pills) the flow works on.

3. What is a data pill?
   A. A scheduled job that fires the flow
   B. A draggable chip that pipes a value from the trigger or an earlier step into a later field
   C. A saved copy of the flow
   D. A notification template
   CORRECT: B
   EXPLAIN: Data pills carry live values — like the order number or customer email — so steps don't hardcode anything.

4. Which of these is a Flow Logic block rather than an Action?
   A. Send Notification
   B. Create Record
   C. For Each
   D. Ask for Approval
   CORRECT: C
   EXPLAIN: For Each controls the route (it loops over items); the others perform work.

5. What should you do BEFORE activating a new flow?
   A. Delete the trigger
   B. Test it against a real record and step through each action
   C. Convert it to a Business Rule
   D. Hardcode all the data pills
   CORRECT: B
   EXPLAIN: Testing runs the flow in a safe sandbox so you can confirm the values and branches before it goes live.

6. What is the purpose of a Stage?
   A. To store computed values
   B. To label and group steps so a long flow reads like a story and is easy to debug
   C. To make the flow run faster
   D. To replace the trigger
   CORRECT: B
   EXPLAIN: Stages are visual (and logged) groupings that make big flows readable and pinpoint the failing part of a run.

7. Where do you look to confirm a flow actually ran and inspect each step?
   A. The business rules table
   B. The flow's Executions log
   C. The customer's email inbox
   D. The form's client scripts
   CORRECT: B
   EXPLAIN: Every run is recorded under Executions, where you can replay the steps and see the runtime values.
