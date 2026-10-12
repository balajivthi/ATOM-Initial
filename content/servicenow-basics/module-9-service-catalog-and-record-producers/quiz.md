# Quiz: Service Catalog & Record Producers

Answer these questions about the service catalog. Your score is saved, and reasoning is revealed after you submit.

1. When a user orders a catalog item, what is created?
   A. Only an email
   B. A Request (REQ) plus a Requested Item (RITM)
   C. A new user account
   D. A transform map
   CORRECT: B
   EXPLAIN: Ordering creates a Request, and each catalog item ordered becomes a Requested Item that the workflow can act on.

2. What are the "questions" on a catalog item's order form called?
   A. Fields
   B. Variables
   C. Sections
   D. Choices
   CORRECT: B
   EXPLAIN: Variables are the questions a user answers when ordering; their answers are stored and can map onto the target record.

3. A Record Producer is best for:
   A. Complex multi-step approvals
   B. Creating a record directly in a target table from a portal form
   C. Importing Excel data
   D. Sending bulk emails
   CORRECT: B
   EXPLAIN: A record producer's variables map straight onto the target table, so ordering it creates a record directly.

4. What can be attached to a catalog item to orchestrate approvals and tasks after ordering?
   A. An ACL
   B. A workflow or Flow
   C. A notification only
   D. An import set
   CORRECT: B
   EXPLAIN: Workflows (or Flows) attached to catalog items drive approvals, tasks and notifications after the order is placed.

5. Which tool lets you preview the order experience as a user would see it?
   A. Preview Email
   B. Try it
   C. Test Transform
   D. Impersonate
   CORRECT: B
   EXPLAIN: "Try it" on a catalog item/record producer opens the item exactly as a user would experience it in the portal.
