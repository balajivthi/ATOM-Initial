# Getting Started with Service Catalog

The **Service Catalog** is how end users request things — a laptop, software, access, a service. This lesson covers **catalog items** and **variables**, the building blocks of a self-service request. (A *Record Producer* — the focus of the next lesson — is a special catalog item that creates a record.)

## What is a Catalog Item?

A catalog item is a "product" in the catalog that users can order. When they order it, a **Request** is created, which in turn creates **Requested Items** (RITMs) — one per catalog item ordered.

```
User orders an item
   └── Request (REQ) created
          └── Requested Item (RITM) for that catalog item
                 └── Workflow may create Tasks, approvals, etc.
```

## Catalog Definitions

- **Catalog** — a grouping of items (e.g. "Hardware", "Software", "Services").
- **Category** — a sub-grouping within a catalog.
- **Catalog item** — the thing users order.
- **Variable** — a question on the item's order form; answers get stored.
- **Variable set** — a reusable group of variables.

## Creating a Catalog Item (Maintain Items)

1. Navigate to **All → Service Catalog → Catalog Definitions → Maintain Items** (or `sc_cat_item.list`).
2. Click **New**.
3. Configure the catalog item form:
   - **Name**: e.g. *Power Bank Request*.
   - **Short description** and **Description** (shown to users).
   - **Catalog** and **Category**: where the item appears.
   - **Price**, **Quantity**, **Delivery** options as needed.
4. Click **Submit**.

## Adding Variables

Variables are the questions the user answers when ordering:

1. Open your catalog item.
2. On the **Variables** related list, click **New**.
3. Create your variables, e.g.:
   - **Power Bank Count** (type: **Integer**).
   - **Requested For** (type: **Reference** to User).
   - **Comments** (type: **Multi-line text**).
4. Set **Order** so the questions appear in a sensible sequence.
5. Click **Submit**.

### Using Variable Sets

If you have the same questions on several items, group them:

1. Create a **Variable Set** (via the variable set related list on an item, or under Catalog Definitions).
2. Add your shared variables to it.
3. On each item's **Variable Sets** related list, click **Edit**, add the set, and adjust its **Order** (e.g. 300) so it appears after the item's own variables.

## Previewing Your Item

Click **Try it** on the catalog item — ServiceNow opens the item as a user would see it, letting you review the order form and test it end to end.

## Lab: Customising with a Workflow

Catalog items can run a **workflow** (or **Flow**) to orchestrate what happens after ordering — approvals, tasks, notifications.

1. Navigate to **All → Process Automation → Workflow → Workflow Editor** (the *Process Engine*).
2. Click **New** (or search), name it `Power Bank Request`, and submit — the workflow canvas opens.
3. Build a basic workflow (e.g. **Begin → Approval → Create Task**).
4. In the workflow toolbar, open **Workflow Actions → Publish** to make it active.
5. Return to the **Maintain Item** and set its **Workflow** to the newly published one.
6. Click **Try it** and place a request.
7. Open the **Requested Items** table (`sc_req_item.list`) and observe the item is **pending approval**.
8. **Impersonate** the requesting user (from your admin user menu) and check **My Approvals**.
9. Ensure the approver user has the **approver_user** role — if not, add it as admin.
10. Impersonate an approver, open **My Approvals**, and **Approve** the record.
11. **End impersonation**, reopen the Requested Item, and observe it is approved and a **new task** was created by the workflow.

## Key Takeaways

- Catalog items are the products users order; variables are the questions they answer.
- Ordering creates a **Request** → **Requested Item** chain.
- **Variable sets** reuse common question groups across items.
- **Try it** lets you test the order experience before going live.
- **Workflows/Flows** attached to items drive approvals, tasks and notifications after ordering.
