# Quiz: The Language of the Platform

Answer these questions about JavaScript basics, where scripts run, and the GlideSystem. Your score is saved, and reasoning is revealed after you submit.

1. Which two places can ServiceNow scripts run?
   A. Server-side and client-side
   B. Mobile and desktop
   C. Frontend and database-only
   D. Batch and realtime only
   CORRECT: A
   EXPLAIN: Scripts run server-side (Business Rules, Script Includes) or client-side (Client Scripts, UI Policies). The JavaScript is the same; the APIs differ.

2. Which comparison operator should you always use in ServiceNow scripts?
   A. ==
   B. =
   C. ===
   D. equals()
   CORRECT: C
   EXPLAIN: `===` is strict equality and avoids the type coercion bugs caused by `==`.

3. What is the quickest safe place to test a server-side script?
   A. A Client Script
   B. Scripts Background
   C. A UI Policy
   D. The Service Portal
   CORRECT: B
   EXPLAIN: Scripts Background (System Definition → Scripts Background) is the sandbox for running server-side logic and reading the output/logs.

4. Which method writes a normal progress message to the system log?
   A. gs.print()
   B. gs.info()
   C. console.log()
   D. gs.notify()
   CORRECT: B
   EXPLAIN: `gs.info(msg)` logs progress; there are also `gs.warn`, `gs.error` and `gs.debug`.

5. How do you read a system property with a fallback value in a script?
   A. gs.getProperty('name', 'default')
   B. gs.property('name')
   C. gs.get('name')
   D. gs.getConfig('name')
   CORRECT: A
   EXPLAIN: `gs.getProperty(name, default)` returns the stored value or the default if the property is missing.

6. The `gs` object in a server-side script is an instance of which API?
   A. GlideRecord
   B. GlideSystem
   C. GlideForm
   D. GlideAjax
   CORRECT: B
   EXPLAIN: `gs` is the GlideSystem — user context, logging, properties, dates and events in one object.
