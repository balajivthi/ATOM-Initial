# Creating Record Producers

A **Record Producer** is a catalog item that, when ordered, **creates a record directly in a table** — skipping the Request/Requested Item chain. It is the quickest way to let end users create records (like a *Place Order* entry) through the portal.

## Record Producer vs Catalog Item

| | Catalog Item | Record Producer |
| --- | --- | --- |
| Creates | Request + Requested Item | A record directly in the target table |
| Best for | Multi-step requests needing approvals | Simple "fill a form → create a record" |
| Navigation | Service Catalog → Catalog Items | Service Catalog → Record Producers |
| Type | `sc_cat_item` | `sc_cat_item_producer` |

> Record producers are also the classic way to build a **data-entry form** for end users: the variables map straight onto the target table's fields.

## Creating a Record Producer

1. Navigate to **All → Service Catalog → Record Producers** (or `sc_cat_item_producer.list`).
2. Click **New**.
3. Configure the form:
   - **Name**: e.g. `Place Order`.
   - **Table**: the table the record is written to, e.g. **Order & Tracking**.
   - **Catalog / Category**: where it appears for ordering.
4. Click **Submit**.

## Mapping Variables to the Target Table

1. Open your record producer.
2. On the **Variables** related list, click **New**.
3. Create a variable for each field you want captured, e.g.:
   - **Order Description** → target field `Description`.
   - **Delivery Date** → target field `Delivery date`.
   - **Agent** (Reference to the Delivery Agents table).
4. For each variable, set its **Name/type**, then click the **variable's question mark** (or the **Field** mapping) so its answer is written to the correct target-table field.

> The core idea: the variable's value becomes the value of the mapped column when the record is created. Configure the "writes to field" mapping so no data is lost.

## Test it from the Service Portal

1. Save the record producer.
2. Open the **Service Portal** (your instance's user portal, e.g. `https://<instance>.service-now.com/sp`).
3. Search the catalog for **Place Order** and order it.
4. Fill in the variables and submit.
5. Open the **Order & Tracking** table (`u_order_tracking.list`) and confirm the record was created with the submitted values.

## Record Producer Options Worth Knowing

| Setting | Purpose |
| --- | --- |
| **Short description** | Shown in the catalog |
| **Show in portal / cart** | Whether it appears for end users |
| **Record script** | Runs before insert — customise values or prevent creation |
| **Transform to the target table** | Map variables to fields automatically |
| **Variables → Writes to** | Which target field each variable fills |

> For advanced use, a **Flow Designer** flow attached to the produced record can notify someone, trigger approvals, or call APIs — giving record producers the automation of catalog items without the Request chain.

## Lab

1. Create a record producer **Place Order** targeting the **Order & Tracking** table.
2. Add variables for order description and delivery date, mapped to the table's fields.
3. Order it from the Service Portal and confirm the record lands in the Order & Tracking list.

## Key Takeaways

- **Record producers** create records directly in a target table when ordered.
- **Variables** are the questions; their answers map to the target table's fields.
- Record producers live in **Service Catalog → Record Producers** (`sc_cat_item_producer`).
- Test from the **Service Portal** to confirm the end-user experience.
- Combine with flows for notifications and follow-up automation.
