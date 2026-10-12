# Quiz: Scripts in the Browser

Answer these questions about Client Scripts, the `g_form` API, and the common patterns. Your score is saved, and reasoning is revealed after you submit.

1. Where does a Client Script execute?
   A. On the platform's server
   B. In the user's browser
   C. In a scheduled job
   D. On a mobile device only
   CORRECT: B
   EXPLAIN: Client Scripts run in the browser using the `g_form` API; Business Rules and Script Includes run server-side.

2. Which event fires when the user changes a specific field on the form?
   A. onLoad
   B. onChange
   C. onSubmit
   D. onUpdate
   CORRECT: B
   EXPLAIN: `onChange` reacts to a specific field's value change; `onLoad` fires when the form opens and `onSubmit` when the form is saved.

3. What is the correct way to block a save and show an error in onSubmit?
   A. throw 'error'
   B. g_form.blockSave()
   C. g_form.addErrorMessage(...) then return false
   D. g_form.setReadOnly('save', true)
   CORRECT: C
   EXPLAIN: The onSubmit pattern is `g_form.addErrorMessage(message)` followed by `return false`, which cancels the save and displays the message.

4. Which method makes a field required at runtime?
   A. g_form.setValue('field', true)
   B. g_form.setMandatory('field', true)
   C. g_form.require('field')
   D. g_form.setDisplay('field', true)
   CORRECT: B
   EXPLAIN: `g_form.setMandatory('field', true)` toggles the required state; `setValue` sets a value and `setDisplay` controls visibility.

5. Why should you never rely on Client Scripts for security?
   A. They are too slow to trust
   B. They run in the browser and can be skipped or bypassed
   C. They only work in the Service Portal
   D. They cannot read field values
   CORRECT: B
   EXPLAIN: Client-side code runs in the user's browser, so it can be disabled or tampered with. Real access control lives server-side in ACLs.

6. What is the `isLoading` guard used for in onChange scripts?
   A. To make the form load faster
   B. To prevent the script from firing while the form is still loading
   C. To block the Save button
   D. To log every change to the server
   CORRECT: B
   EXPLAIN: `if (isLoading) return;` stops onChange logic from running during the initial form render, before the user has changed anything.
