# Working with Tables

Applications in ServiceNow are built on **custom tables**. This lesson shows how to create a table, add columns, and make it appear as an application in the navigation — the first step in building your own mini-app.

## What is a Table?

A **table** stores records of one type. Every table lives in the database and is configured via the **Table** record (`sys_db_object`). When you create a table, ServiceNow also generates:

- A **form** and **list** for the records.
- A set of system **columns** (created, updated, sys_id, and so on).
- An entry in the **application navigator** (if you choose Create Module).

## Creating a Table

1. Navigate to **All → System Definition → Tables** (or `sys_db_object.list`).
2. Click **New**.
3. Give the table a **Label**, e.g. `Order & Tracking`.
4. Under **Control**:
   - Check **Auto Number** — this adds a system-generated sequential **Number** field (like `ORD0010001`) used as a human-friendly reference.
   - **Uncheck Create access control** — by default the platform creates basic ACLs for you; turning this off means the table is only accessible to users you explicitly grant access (a useful teaching step).
5. Under **Create Module**, give a module name such as `Delivery App`. This creates an application entry in the navigation with your table under it.
6. Click **Submit**.

> Observe the result: the new table comes with around **7 system columns** (Sys ID, Number, Created by/on, Updated by/on, etc.) ready to use.

## Adding Columns (Fields)

1. Open your table record.
2. On the **Columns** related list, click **New** to add a field.
3. Configure:
   - **Label**: e.g. *Delivery Date*.
   - **Type**: string, integer, date/time, choice, reference (link to another table), etc.
   - **Max length** and other properties as needed.
4. Click **Submit**.

### Reference fields link tables

A field of type **Reference** points to records in another table — for example, a *Delivery Agent* column referencing your Agents table. This is how tables become relational.

## Table Details You Should Know

| Setting | Purpose |
| --- | --- |
| **Label** | Human-readable name (can be pluralised for lists) |
| **Name** | Internal table name (e.g. `u_order_tracking` for custom tables) |
| **Auto Number** | Adds a Number column with a sequence |
| **Extends** | Class inheritance — extend `Task` to inherit task fields |
| **Application** | Which application the table belongs to |
| **Create Module** | Adds a navigation module for the table's list |
| **Create access control** | Auto-generates basic read ACLs for the table |

> Custom tables use the `u_` name prefix (e.g. `u_order_tracking`) to avoid collisions with OOTB tables.

## Lab

1. Create a table labeled **Order & Tracking** with Auto Number on and Create access control off; module **Delivery App**.
2. Add a column, e.g. **Delivery Date** (Date/time type) and **Status** (Choice type).
3. Create a second table labeled **Delivery Agents** (same module `Delivery App`, Control role = `app_support_user`).
4. Open the module in the filter navigator and confirm both lists appear under **Delivery App**.

## Key Takeaways

- Tables are the foundation of custom apps; each gets a form, list and system columns.
- **Auto Number** gives records a sequential reference number.
- **Create Module** exposes the table in the application navigator.
- Fields can be strings, choices, date/times or **references** to other tables.
- Custom tables carry the `u_` prefix to stay separate from OOTB tables.
