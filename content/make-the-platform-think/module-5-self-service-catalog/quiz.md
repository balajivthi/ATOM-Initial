# Quiz: Self-Service Catalog

Answer these questions about catalog items, catalog variables, and Catalog Client Scripts. Your score is saved, and reasoning is revealed after you submit.

1. What does a Catalog Item create when a user orders it?
   A. A record on the sys_user table
   B. A Request
   C. An email
   D. A Business Rule
   CORRECT: B
   EXPLAIN: A Catalog Item creates a Request when ordered. A Record Producer creates a record on a specific table (and can also create a Request).

2. How do you reference a catalog variable named `order_number` in a classic `g_form` script?
   A. g_form.getValue('order_number')
   B. g_form.getValue('variable_order_number')
   C. g_form.getValue('u_order_number')
   D. g_form.getValue('sysvar.order_number')
   CORRECT: B
   EXPLAIN: Catalog variables use the `variable_` prefix in `g_form` calls. The `catalyst` API lets you use the plain name without the prefix.

3. Which API is catalog-aware and lets you use plain variable names?
   A. g_form
   B. g_user
   C. catalyst
   D. glideForm
   CORRECT: C
   EXPLAIN: `catalyst` wraps the catalog form so variables are addressed by plain name (e.g. `catalyst.getValue('order_number')`).

4. Which event would you use to show a photo field only when the issue type is "damaged"?
   A. onLoad
   B. onChange
   C. onSubmit
   D. onShow
   CORRECT: B
   EXPLAIN: `onChange` on the issue-type variable reacts as the user selects a value, so the photo question can appear immediately.

5. Where should a Catalog Client Script be attached so it runs on every item that reuses common logic?
   A. A table
   B. A Variable Set
   C. A Record Producer
   D. An ACL
   CORRECT: B
   EXPLAIN: Attaching a script to a Variable Set applies it to every catalog item that includes that set — reuse without duplication.

6. Which approach best turns a "Report a Delivery Issue" catalog item into a row on the Delivery App table?
   A. A Client Script
   B. A Record Producer
   C. A UI Policy
   D. A scripted REST API
   CORRECT: B
   EXPLAIN: A Record Producer creates a record on a chosen table from the submitted variables, landing the report directly in `u_order_tracking`.
