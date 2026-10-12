# Quiz: Email Notifications

Answer these questions about notifications. Your score is saved, and reasoning is revealed after you submit.

1. Which notification setting sends the email when a record is CREATED?
   A. Deleted
   B. Inserted
   C. Updated
   D. Assigned
   CORRECT: B
   EXPLAIN: On the "When to send" tab, the Inserted checkbox triggers the notification when a record is created.

2. Where do you verify that a notification actually fired?
   A. The Activity log on the record
   B. System Logs → Emails
   C. The All menu
   D. The user's inbox inside ServiceNow
   CORRECT: B
   EXPLAIN: Sent emails are recorded in System Logs → Emails, where you can search by subject and open/Preview Email.

3. On the "Who will receive" tab, recipients CANNOT be:
   A. A single user
   B. A role
   C. A group
   D. A random phone number
   CORRECT: D
   EXPLAIN: Recipients are resolved from the platform — users, roles, groups, or dynamic values on the record — not arbitrary phone numbers.

4. How do you preview the exact email a recipient would see?
   A. Forward the email to yourself
   B. Open the email record in System Logs → Emails and click Preview Email
   C. Print the notification record
   D. Ask a user to send you a screenshot
   CORRECT: B
   EXPLAIN: Preview Email renders the message as the recipient would receive it, using the actual record's values.

5. In the message body, how do you insert a field value from the record?
   A. Type the field name in square brackets, e.g. [number]
   B. Use the field picker to insert it, e.g. ${number}
   C. Paste a screenshot of the field
   D. It is impossible
   CORRECT: B
   EXPLAIN: Field values are inserted with the field picker (rendering like ${number}) so emails personalise with record data.
