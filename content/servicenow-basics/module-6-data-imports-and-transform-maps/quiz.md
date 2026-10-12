# Quiz: Data Imports & Transform Maps

Answer these questions about importing data. Your score is saved, and reasoning is revealed after you submit.

1. What is the FIRST stage of a ServiceNow data import?
   A. Writing records straight into the business table
   B. Staging raw rows into an import set table
   C. Sending an email to the data owner
   D. Creating an ACL
   CORRECT: B
   EXPLAIN: Imports are two-stage: rows are first staged into an import set table, then transformed into the real business table.

2. What does a Data Source definition specify?
   A. Where data comes from and how it is read (format, sheet, header row)
   B. Who is allowed to see the data
   C. Which users will be notified
   D. How long the import should take
   CORRECT: A
   EXPLAIN: A data source defines the file/format/source (e.g. Excel, sheet number, header row); loading then reads the file into the import set.

3. What moves import set rows into the business table?
   A. A business rule
   B. A transform map
   C. An email notification
   D. A scheduled job only
   CORRECT: B
   EXPLAIN: The transform map maps source columns to target fields and applies rules (including coalesce) as it inserts/updates records.

4. What does setting "Coalesce = True" on a field prevent?
   A. Empty rows
   B. Duplicate records in the target table
   C. Errors in the log
   D. Slow imports
   CORRECT: B
   EXPLAIN: Coalesce identifies a unique field; when rows share that value, the existing record is updated instead of inserting a duplicate.

5. A transform outcome of "Inserted" means:
   A. The import was cancelled
   B. A new record was created in the target table
   C. The row was ignored
   D. The file was deleted
   CORRECT: B
   EXPLAIN: Outcomes are Inserted (new record), Updated (coalesce matched an existing record), Ignored, or Error.
