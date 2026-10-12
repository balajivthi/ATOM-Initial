# Working with Transform Maps

Once raw data sits in an **import set table**, a **transform map** moves it into the real business table — mapping fields, applying rules and preventing duplicates. This is where the magic of the Day 6 lab happens.

## What a Transform Map Does

A transform map connects a source (import set) table to a target (business) table:

- **Maps source columns → target fields** (manually or automatically by matching names).
- **Coalesce** — chooses a unique field to detect duplicates and avoid creating them twice.
- Runs **scripts** and field mappings to clean the data during the move.
- Produces an outcome per row: Inserted, Updated, Ignored or Error.

## Creating a Transform Map

1. Open the **Data Source** you created in the previous lesson.
2. On the **Transform** related list, click **New**.
3. Configure:
   - **Name**: e.g. `Transform Delivery Agent Data`.
   - **Target table**: the real business table, e.g. `Delivery Agents`.
4. Click **Submit** — you return to the data source, and the transform map now appears in its related list.

## Load and Auto-Map

1. On the data source, click **Load all records** to stage the Excel rows (if not already loaded).
2. Open the newly created **Transform Map**.
3. Click **Auto Map Matching Fields** — ServiceNow matches source columns to target fields automatically **when the names are similar**.
4. Review the resulting field mappings and fix any that were guessed incorrectly.

## Coalesce: Preventing Duplicates

**Coalesce** tells the transform map which field uniquely identifies a record. When multiple rows share the same coalesced value, ServiceNow **updates the existing record instead of inserting a new one**.

In the Day 6 lab, the Excel file had a `Delivery Agent` field that already existed as one record in the target table:

1. In the transform map's **Field Mappings**, double-click the **Coalesce** column for the agent field and change it from **False** to **True**.
2. Save the field mapping.

> Without coalesce: 10 Excel rows + 1 existing record = 11 records. With coalesce on the agent field: duplicates collapse, and only **unique** records are created.

## Running the Transform

1. Click **Transform** on the transform map (or from the data source).
2. On the **Specify Import Set and Transform Map** page, note the **Import Set** number and **Transform Map** name.
3. Click **Transform**.
4. Wait for the **progress page** to complete.
5. Open the target table's list and verify the outcome — unique rows created, duplicates ignored/updated.

## Interpreting Outcomes

| Outcome | Meaning |
| --- | --- |
| **Inserted** | New record created in the target table |
| **Updated** | Existing record updated (matched by coalesce) |
| **Ignored** | Skipped (e.g. blank or coalesce conflict) |
| **Error** | Transform failed for this row — check the logs |

## Lab

1. Create the transform map **Transform Delivery Agent Data** targeting the **Delivery Agents** table.
2. Click **Auto Map Matching Fields** and review the mappings.
3. Set **Coalesce = True** on the agent field.
4. Run the transform and confirm the record count matches the expectation: 10 Excel rows, 1 existing record → only unique records in the target.

## Key Takeaways

- Transform maps move import set rows into business tables via **field mappings**.
- **Auto Map Matching Fields** speeds mapping when source and target names match.
- **Coalesce** on a unique field prevents duplicate records.
- Transforms report per-row outcomes (Inserted/Updated/Ignored/Error) — always review the results.
