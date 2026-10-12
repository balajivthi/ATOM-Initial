# Quiz: Run It for Real

Answer these questions about reusable blocks, tool choices, and monitoring. Your score is saved, and reasoning is revealed after you submit.

1. What is a subflow?
   A. A trigger that fires on a schedule
   B. A triggerless routine of steps with inputs and outputs, callable from other flows
   C. A type of notification template
   D. A client-side script block
   CORRECT: B
   EXPLAIN: A subflow is a reusable "mini-flow" — no trigger, defined inputs/outputs, called from other flows.

2. What is the key difference between a custom action and a subflow?
   A. Custom actions can't take inputs
   B. A custom action wraps one atomic job; a subflow is a multi-step routine
   C. Subflows can't return outputs
   D. Only subflows appear in the action picker
   CORRECT: B
   EXPLAIN: Custom actions are single reusable operations (wrap a script or REST call); subflows are multi-step routines.

3. When is the best time to extract repeated logic into a reusable block?
   A. Never — always copy-paste
   B. On the first copy
   C. On the second copy (repetition confirmed)
   D. Only after a bug is reported
   CORRECT: C
   EXPLAIN: The second occurrence confirms genuine repetition; extract then so there's one source of truth.

4. You must stop a record from saving when it's invalid. Which tool fits?
   A. A flow
   B. A before Business Rule
   C. A Client Script alone
   D. A scheduled job
   CORRECT: B
   EXPLAIN: Only a "before" Business Rule runs before the write and can abort it — flows are asynchronous and after the fact.

5. Nightly "chase all overdue orders" work is multi-step and should be maintainable and logged. What's the best fit?
   A. A Client Script
   B. A legacy Workflow
   C. A scheduled flow
   D. A UI Policy
   CORRECT: C
   EXPLAIN: A scheduled flow gives visual steps, logging, and maintainability for recurring multi-step work.

6. A flow runs but sends an email with blank fields. Where do you look first?
   A. The customer's spam folder
   B. The execution log — the inputs of the notification step (a data pill is empty)
   C. The form's client scripts
   D. The database schema
   CORRECT: B
   EXPLAIN: Debug from the failed/incorrect step's inputs; a blank field usually means an empty data pill upstream.

7. A flow executes twice for a single record change. Most likely cause?
   A. The trigger table is wrong
   B. The run mode is "for each update" where "Once" was intended
   C. The flow has too many stages
   D. It lacks a custom action
   CORRECT: B
   EXPLAIN: Duplicate runs usually come from the trigger's run mode, not the logic — fix it at the source.

8. Why should you be careful when replaying an execution after a fix?
   A. Replay is not allowed
   B. The flow will run its actions again, possibly duplicating side effects
   C. Replay deletes the flow
   D. Replay changes the trigger table
   CORRECT: B
   EXPLAIN: Replay re-runs the flow against the same record, so real side effects (tasks, emails) can occur twice — design idempotent steps.
