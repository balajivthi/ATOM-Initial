# Quiz: Tables & ACLs

Answer these questions about tables and access control. Your score is saved, and reasoning is revealed after you submit.

1. What does the "Auto Number" setting do on a new table?
   A. Auto-fills every field
   B. Adds a system-generated, sequential Number field for each record
   C. Creates 7 new columns automatically
   D. Hides the table from users
   CORRECT: B
   EXPLAIN: Auto Number adds a Number column (like ORD0010001) that is generated sequentially for each new record.

2. You create a table with "Create access control" UNCHECKED. What happens?
   A. Everyone can access it
   B. Only admins can access it — there are no ACLs granting access
   C. It cannot be created
   D. It appears only in the Service Portal
   CORRECT: B
   EXPLAIN: ACLs are default-deny. With no ACLs created, only users with the admin role (which bypasses ACLs) can access the table.

3. Custom tables get which name prefix to avoid clashing with OOTB tables?
   A. x_
   B. c_
   C. u_
   D. t_
   CORRECT: C
   EXPLAIN: Custom (user-created) tables use the `u_` prefix, e.g. `u_order_tracking`.

4. What is the default behaviour of ACL-based security?
   A. Allow everything unless blocked
   B. Deny by default unless a rule grants access
   C. Ask for a password
   D. Only protect admin tables
   CORRECT: B
   EXPLAIN: If no ACL grants access, the operation is denied — that is why roles and ACLs must be configured deliberately.

5. Which of these is an ACL "type"?
   A. read
   B. copy
   C. paste
   D. rename
   CORRECT: A
   EXPLAIN: ACLs come in four types — read, write, create and delete.
