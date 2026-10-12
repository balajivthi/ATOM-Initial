# Quiz: Rules of the Game

Answer these questions about Business Rules. Your score is saved, and reasoning is revealed after you submit.

1. What triggers a Business Rule to run?
   A. A user clicking a button only
   B. A record being inserted, updated, or deleted on its table
   C. A scheduled job only
   D. An email being sent
   CORRECT: B
   EXPLAIN: Business Rules run automatically when records on the configured table are inserted, updated, or deleted.

2. Which rule type runs BEFORE the record is written to the database?
   A. After update
   B. Before insert/update
   C. Async
   D. Display
   CORRECT: B
   EXPLAIN: Before rules run before the save, so they can set defaults or abort the operation with setAbortAction(true).

3. What does `previous` represent in a Business Rule script?
   A. The next record to be processed
   B. The record's state before the current operation
   C. The logged-in user
   D. The current table name
   CORRECT: B
   EXPLAIN: `previous` is a snapshot of the record before this operation — ideal for detecting field changes. It is null on insert.

4. How do you prevent a save inside a "before" Business Rule?
   A. current.deleteRecord()
   B. current.setAbortAction(true)
   C. gs.abort()
   D. return false
   CORRECT: B
   EXPLAIN: `current.setAbortAction(true)` blocks the save; pair it with gs.addErrorMessage() to tell the user why.

5. Where should you create a related record (e.g. a task) when an order is inserted?
   A. In a "before" rule
   B. In an "after" rule
   C. In a display rule
   D. In a client script
   CORRECT: B
   EXPLAIN: After rules run once the record is saved — the right time to spawn related records like tasks.

6. Which practice helps avoid Business Rule recursion?
   A. Calling current.update() in every rule
   B. Using conditions and `previous` guards, and moving self-table writes to async
   C. Hardcoding sys_ids
   D. Querying inside a while loop
   CORRECT: B
   EXPLAIN: Guards on the change, careful conditions, and async execution prevent a rule from re-triggering itself.
