# Bring the Batch

**Story so far:** Real-time events handle the "van delivered" moments. But every morning the van partner hands over something big and slow: **today's full manifest** — a CSV of every scheduled delivery. There's no event for "here are 4,000 rows." That's a **batch integration**, and it has its own pipeline.

## Batch vs Real-Time

| | Real-time (webhook) | Batch (file/import) |
| --- | --- | --- |
| Volume | One event | Thousands of rows |
| Trigger | Partner pushes | A schedule (e.g. 06:00) |
| GlidePort side | An endpoint | An **Import Set** pipeline |
| Use for | Delivered, failed, changed | Manifests, reconciliations, migrations |

You met Import Sets and Transform Maps in *Introduction to ServiceNow*. Now we use them as an **integration** tool.

## The Import Pillars

Every file-based integration is the same three-stage pipeline:

```
[ Data Source ]  ─▶  [ Import Set (staging) ]  ─▶  [ Transform Map ]  ─▶  Target records
   where it         raw rows land, untouched        map + coalesce        u_order_tracking
   comes from       (safe to re-run)                + validation
```

1. **Data Source** — *where the file comes from*: a File/CSV attachment, an FTP/SFTP location, a URL. (`sys_data_source`)
2. **Import Set** — *a staging table* where rows land as-is. Untouched, auditable, re-runnable.
3. **Transform Map** — *the mapping*: which source column becomes which target field, plus **coalesce** and scripts.

The isolation is deliberate: bad rows land in staging and **don't touch real data** until a transform succeeds.

## Step 1 — A Data Source for the Manifest

1. **All → System Import Sets → Data Sources → New**.
2. **Name:** `Van partner daily manifest`
3. **Type:** File / CSV (or the FTP/URL variant your partner uses)
4. Point it at the file (or a folder the partner uploads to).

## Step 2 — Load It Into a Staging Table

"Loading" copies the rows into an import set. You can load on demand or on a schedule. Define an **Import Set Table** whose columns mirror the file:

| CSV column | Staging column |
| --- | --- |
| `tracking` | `u_tracking` |
| `status` | `u_status` |
| `expected` | `u_expected` |
| `agent` | `u_agent` |

## Step 3 — Transform Into Orders

The **Transform Map** connects staging → target. The star setting is **coalesce**:

> **Coalesce** = "match an existing target record on these fields, then **update** it; otherwise **insert**."

Set coalesce on `tracking` so a manifest row **updates** the order that already exists instead of creating a duplicate:

```js
// onAfter transform script (runs per row)
if (target.u_status.changes()) {
    target.u_last_manifest_sync = new GlideDateTime();
}
```

Then decide the **coalesce policy** for the empty case: create, skip, or (usually) create-once.

## Step 4 — Schedule It

Batch integrations run on a clock. Chain two scheduled jobs (recap of *Scheduling Data Imports* from the basics course):

1. **Load Data** — pull the file into an import set.
2. **Transform** — run the transform map on the new import set.

```
06:00  Load Data      → import set #4491 (4,000 rows)
06:01  Transform      → coalesce-updates u_order_tracking
```

## Handling Bad Rows

A good pipeline tells you *what* went wrong, per row:

- Each import set row carries an **error** field; failed rows are **not** dropped silently.
- Use **onBefore** scripts to validate/skip gracefully, and **onAfter** scripts for related records.
- Review the **Import Set Run** history: rows loaded, rows transformed, rows with errors.
- Fix the source data (or the map) and **re-run** — staging is safe to reprocess.

| Problem | Where to look |
| --- | --- |
| Expected 4,000 rows, got 0 | Data source path / file access |
| Rows loaded, none transformed | Transform map's condition or coalesce policy |
| Duplicates created | Coalesce field not set (or not unique) |
| Fields blank | Column mapping missing/wrong |

## When to Use Batch

- The partner **offers a file** and no real-time API.
- You need a **reconciliation** (make GlidePort match their truth).
- One-time **migration** of historical data.

For events, prefer the inbound endpoint from the previous lesson.

## Lab: Reconcile the Daily Manifest

1. Create a CSV with 5 rows (`tracking,status,expected,agent`) including **one tracking number that already exists** in your orders.
2. Build the Data Source, Import Set table, and Transform Map with **coalesce on `tracking`**.
3. Load and transform. Confirm: existing orders are **updated**, new ones are **created**, none duplicated.
4. Add a deliberately malformed row and confirm it lands in staging with an **error**, without corrupting target records.
5. Create the two scheduled jobs (Load + Transform).

**Check your work:** re-running the same file twice leaves the same number of records (coalesce upserts); bad rows are isolated in staging with errors.

## Key Takeaways

- **Batch** integrations land large data sets on a schedule via the **Import Set pipeline**.
- Three stages: **Data Source → Import Set (staging) → Transform Map → target**.
- Staging isolates bad data; real records are only touched by a successful transform.
- **Coalesce** turns a "load" into an **upsert** — update existing, create new.
- Schedule **Load** then **Transform**, and always check the run history for errors.

## Best Practices

- Always set **coalesce** on a stable key so re-runs don't duplicate.
- Keep staging tables **as close to the raw file** as possible — no business logic there.
- Validate in **onBefore**; do related work in **onAfter**; keep transforms idempotent.
- Review import errors every run; a silently failing transform is worse than a loud one.
