# Configuring Email Notifications

**Notifications** are how ServiceNow tells people something happened — an email when a record is created, updated or assigned, for example. They are configuration, not code, and they are one of the most-used admin features.

## The Anatomy of a Notification

A notification record (in **System Notification → Email → Notifications**) answers three questions:

| Question | Field/Tab |
| --- | --- |
| **When?** | The *When to send* tab — which record events trigger it (inserted, updated, deleted, assignment…) |
| **Who?** | The *Who will receive* tab — users, roles, groups, or dynamic recipients from the record |
| **What?** | The *What it will contain* tab — subject and message body (plain text or HTML) |

## Creating a Notification

1. Navigate to **All → System Notification → Email → Notifications** (or `sysevent_email_action.list`).
2. Click **New**.
3. On the **When to send** tab:
   - **Name**: e.g. `Send order info`.
   - **Table**: select the table that triggers it, e.g. **Order & Tracking**.
   - **Condition / event**: check **Inserted** (send when a record is created).
4. On the **Who will receive** tab:
   - Choose a **User** (e.g. a demo user) so you can test the email easily.
   - (In production you'd usually send to the *Caller*, *Assigned to*, or a *Group* on the record.)
5. On the **What it will contain** tab:
   - **Subject**: e.g. `Order {number} has been placed`.
   - **Message HTML**: the email body, using **field values** from the record (e.g. `Order ${order.description}`).
6. Click **Submit**.

## Testing the Notification

1. Open the **Order & Tracking** table (`u_order_tracking.list`).
2. Click **New** and create a record — this **inserts** a row, which fires the notification.
3. Navigate to **All → System Logs → Emails** (or `sys_email.list`).
4. Search for emails with the subject you configured in step 5.
5. Open the email record and click **Preview Email** (related link) to see exactly what the recipient would receive.

## Understanding the "Who Will Receive" Options

| Option | Use when |
| --- | --- |
| **User** | A specific person (great for testing) |
| **Roles** | Everyone holding a role (e.g. all `admin`) |
| **Groups** | The members of a group |
| **Caller / Requested for** | The person who raised the record |
| **Assigned to** | The agent now responsible for the record |
| **Record watch list** | People watching the record |
| **Conditions** | Dynamically calculated recipients |

## Notification Body Tricks

- Insert **field values** with the field-picker (e.g. `${number}`, `${caller.name}`).
- Add **tables/links** so recipients can jump straight to the record.
- Use **HTML** formatting in the Message HTML field for branded emails.
- Reuse a shared **HTML template** for consistent styling across notifications.

> Notifications can also be sent to **Slack/Teams** via integrations, and large-scale messaging is often handled by **Notification > events** combined with **Subscriptions**.

## Lab

1. Create a notification **Send order info** on the **Order & Tracking** table, triggered on **Inserted**.
2. Send it to a **User** (the demo user created in the Users lesson).
3. Set the subject to `Order {number} has been placed` and write a short body with the order description.
4. Create an order record to trigger it.
5. Verify in **System Logs → Emails** and **Preview Email**.

## Key Takeaways

- Notifications = **when** (events) + **who** (recipients) + **what** (subject/body).
- Test emails by targeting a single user and checking **System Logs → Emails**.
- Recipients can be users, roles, groups, or dynamic values from the record.
- Insert record field values into the subject/body for personalised emails.
- Use **Preview Email** to verify formatting before going live.
