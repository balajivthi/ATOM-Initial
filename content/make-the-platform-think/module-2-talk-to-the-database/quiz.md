# Quiz: Talk to the Database

Answer these questions about querying and writing records with GlideRecord. Your score is saved, and reasoning is revealed after you submit.

1. Which GlideRecord method loads exactly ONE record by field value?
   A. query()
   B. get()
   C. next()
   D. initialize()
   CORRECT: B
   EXPLAIN: `get(field, value)` (or `get(sys_id)`) loads a single record and returns true/false; `query()` prepares many records.

2. Which pair is used to iterate over many matching records?
   A. initialize() + insert()
   B. query() + next()
   C. addQuery() + get()
   D. update() + updateMultiple()
   CORRECT: B
   EXPLAIN: `query()` runs the query and `next()` advances through the matching records until none remain.

3. How do you read a field's value from a loaded record as a string?
   A. record.field.toString()
   B. record.getValue('field')
   C. record.read('field')
   D. record.value('field')
   CORRECT: B
   EXPLAIN: `getValue('field')` returns the field value as a string; `getDisplayValue()` returns the display value of reference fields.

4. Which method adds a filter condition to a GlideRecord query?
   A. filter()
   B. where()
   C. addQuery()
   D. select()
   CORRECT: C
   EXPLAIN: `addQuery(field, operator, value)` adds a condition; chain them for AND and use addOrCondition for OR.

5. What does `insert()` return on a GlideRecord?
   A. true/false
   B. The new record's sys_id
   C. The record number
   D. Nothing
   CORRECT: B
   EXPLAIN: `insert()` saves the record and returns its sys_id — useful for linking related records afterward.

6. What does `updateMultiple()` do?
   A. Updates only the current record
   B. Applies the set values to every record matching the query
   C. Deletes all records
   D. Inserts several records at once
   CORRECT: B
   EXPLAIN: `updateMultiple()` applies the field values set on the cursor to the entire result set in one pass.
