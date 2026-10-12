# Quiz: Script Includes & the AJAX Pattern

Answer these questions about Script Includes and client-callable code (GlideAjax). Your score is saved, and reasoning is revealed after you submit.

1. What is a Script Include?
   A. A browser-side JavaScript file
   B. A reusable server-side class (or library) of code
   C. A type of email notification
   D. A scheduled data import
   CORRECT: B
   EXPLAIN: Script Includes (sys_script_include) are server-side, reusable classes. Client Scripts run in the browser; notifications and imports are different features.

2. Which base class do you extend to make a Script Include callable from the browser via GlideAjax?
   A. Class
   B. AbstractAjaxProcessor
   C. GlideRecord
   D. GlideSystem
   CORRECT: B
   EXPLAIN: Extending `AbstractAjaxProcessor` (plus checking the "Client callable" box) is what lets GlideAjax invoke methods on the include.

3. How does a GlideAjax call tell the server which method to run?
   A. It calls the URL directly
   B. Via the `sysparm_name` parameter
   C. Via the method's return value
   D. It cannot; only the first method runs
   CORRECT: B
   EXPLAIN: The client passes `ga.addParam('sysparm_name', 'methodName')`; the server reads params with `this.getParameter('sysparm_...')`.

4. How do you read a custom parameter named `order_number` inside the server method?
   A. request.getParameter('order_number')
   B. this.getParameter('sysparm_order_number')
   C. gs.getParameter('order_number')
   D. g_form.getValue('order_number')
   CORRECT: B
   EXPLAIN: Server-side ajax methods read input via `this.getParameter('sysparm_order_number')` — params are always prefixed with `sysparm_`.

5. Why is the GlideAjax callback described as asynchronous?
   A. It pauses the browser until the server replies
   B. The page keeps working and the answer arrives later
   C. It only runs at midnight
   D. It runs on the server, not the browser
   CORRECT: B
   EXPLAIN: `getXMLAnswer(callback)` returns immediately and the callback fires when the server responds — no page blocking or reload.

6. When running a client-callable Script Include, which user's permissions apply?
   A. The system administrator
   B. The web service user
   C. The currently logged-in user
   D. No user — permissions are skipped
   CORRECT: C
   EXPLAIN: GlideAjax executes as the current user, so roles and ACLs still apply. Never assume client-side exposure is safe.
