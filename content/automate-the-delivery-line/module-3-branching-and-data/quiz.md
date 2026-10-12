# Quiz: Branching and Data

Answer these questions about flow logic, data, and error handling. Your score is saved, and reasoning is revealed after you submit.

1. Which flow logic block loops over a set of records?
   A. If
   B. For Each
   C. Wait for condition
   D. Parallel
   CORRECT: B
   EXPLAIN: For Each iterates a list (often from a Look Up Records action), running its inner steps once per item.

2. What happens when a For Each loops over an empty list?
   A. The flow errors out
   B. The loop body is skipped and the flow continues
   C. The trigger re-fires
   D. An approval is requested
   CORRECT: B
   EXPLAIN: Looping over zero items simply does nothing — safe, but silent, so add an If if "empty" matters.

3. Where must a value be created relative to where it is used as a data pill?
   A. Anywhere on the canvas
   B. Above (earlier than) the step that uses it
   C. Only in the trigger
   D. Only in a Catch block
   CORRECT: B
   EXPLAIN: Values flow downhill; a step can only consume pills produced earlier in the flow.

4. You need one computed delivery window reused by three later notifications. What should you use?
   A. Three separate Script steps
   B. A flow variable set once and read as a pill three times
   C. A hardcoded string
   D. A new trigger
   CORRECT: B
   EXPLAIN: Flow variables store a value under a name so it can be computed once and reused across steps and branches.

5. When should you reach for a Script action?
   A. Before checking whether an action already exists
   B. Only when no ready-made action covers the job
   C. For every step, to be safe
   D. Never; flows can't use scripts
   CORRECT: B
   EXPLAIN: Check the action library first; Script is the escape hatch for the gaps, and repeated script logic should become a custom action.

6. What does a Try/Catch block do?
   A. Runs the Catch always, before the Try
   B. Runs the Try's steps, and the Catch only if one of them fails
   C. Makes the flow run faster
   D. Replaces the trigger
   CORRECT: B
   EXPLAIN: Catch is the failure path — it executes only when a step inside the Try raises an error.

7. A Catch block that only logs and does nothing else is a problem because…
   A. Logs cost money
   B. The flow may appear to succeed while the real work never happened
   C. It makes the flow run twice
   D. It disables the trigger
   CORRECT: B
   EXPLAIN: Silent swallowing hides failures; a Catch should log with detail, alert a human, and/or recover.

8. Why should flow steps be idempotent?
   A. So they run faster
   B. Because async flows can overlap or re-fire, and running twice must not double the effect
   C. Because data pills require it
   D. To avoid using stages
   CORRECT: B
   EXPLAIN: Scheduled re-runs and overlapping updates are normal; idempotent steps (check-before-create, set rather than increment) stay correct.
