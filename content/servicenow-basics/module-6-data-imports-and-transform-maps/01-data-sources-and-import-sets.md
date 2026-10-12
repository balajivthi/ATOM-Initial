# Data Sources and Import Sets

Importing data from Excel, CSV or other systems is one of the most common admin tasks. ServiceNow does this in two stages: first the data is staged into an **import set table**, then a **transform map** moves it into the real table. This lesson covers the first stage.

## The Two-Stage Import Model

```
External file (Excel/CSV)
        │  Data Source
        ▼
Import Set table  (staging area — raw data only)
        │  Transform Map
        ▼
Real business table (e.g. Delivery Agents)
```

Why stage the data at all? Because raw imported rows rarely map cleanly onto a real table — you need to clean, merge and de-duplicate them first. The import set gives you a safe place to inspect the data before transforming it.

## Key Concepts

| Term | What it is |
| --- | --- |
| **Data Source** | The definition of where data comes from (file, URL, SFTP, JDBC…) |
| **Import Set table** | A temporary table where the raw rows land |
| **Import Set** | A single run of loaded rows into the import set table |
| **Transform Map** | The mapping/rules that move rows from import set → business table |

## Creating a Data Source

1. Navigate to **All → System Import Sets → Administration → Data Sources** (or `sys_data_source.list`).
2. Click **New**.
3. Configure:
   - **Name**: e.g. `Delivery Agents data source`.
   - **Import Set table label**: e.g. `Delivery Agents Data` (this becomes the staging table name).
   - **Format**: **Excel**.
   - **Sheet Number**: the worksheet containing the data (often 1).
   - **Header Row**: the row number containing column headers (usually 1).
4. Click **Submit** and **Update** to save.

## Attaching the Data and Loading Rows

1. Open your data source record.
2. In the **Attachments** related list, attach the Excel/CSV file containing your data.
3. Click the **Load all records** related link — ServiceNow reads the file and writes every row into the **import set table**.
4. Open the import set table (find it under **System Import Sets → Import Sets**) and confirm the raw rows are staged, each with an import set row status.

## Inspecting Import Set Rows

Each staged row shows:

- The **Import set** it belongs to.
- The **State**: `Not processed` / `Ignored` / `Inserted` / `Updated` / `Error`.
- The **Data row** values as they arrived (untransformed).

## Lab

1. Create a data source named **Delivery Agents data source** (format Excel, sheet 1, header row 1).
2. Attach a small Excel file with agent data (10 rows).
3. Click **Load all records**.
4. Open the **Delivery Agents Data** import set and confirm 10 rows staged with state **Not processed**.
5. Don't transform yet — that's the next lesson.

## Key Takeaways

- Imports are **two-stage**: staging into an import set, then transforming into the business table.
- A **Data Source** defines the file/format; loading reads the file into the import set table.
- **Import set rows** start as *Not processed* until a transform map acts on them.
- Inspect staged data before transforming to catch bad rows early.
