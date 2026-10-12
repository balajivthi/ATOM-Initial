# Beyond Flat Files

**Story so far:** Events and files cover most of GlidePort's needs. But some data must stay **in sync continuously** — the partner's live van locations, or a customer list that changes all day. Polling every minute is wasteful; a nightly file is too late. This lesson is the spectrum of inbound mechanisms, and how to choose.

## The Refresh Mechanisms

| Mechanism | Freshness | Best for |
| --- | --- | --- |
| **Webhook / inbound event** | Instant | Discrete events (delivered, failed) |
| **Real-time API pull** | On demand | Look up one record when needed |
| **Data Stream / Stream Connect** | Near-continuous | Keep records in sync as changes happen |
| **REST-based Data Source** | Scheduled | A JSON feed pulled on a clock |
| **File import (CSV)** | Scheduled | Bulk manifests, reconciliation |

There's no single "best" — pick by **freshness needs** vs **volume** vs **partner capability**.

## REST-Based Data Sources

A **Data Source** doesn't have to be a file. It can **pull from an API** on a schedule, landing JSON into a staging table, exactly like a CSV:

```
[ REST Data Source ] ─▶ [ Import Set ] ─▶ [ Transform Map ] ─▶ records
   GET partner API        stage JSON        map + coalesce
   (uses an alias for auth)
```

Why this is powerful: you reuse the **entire import pipeline** (staging, coalesce, validation, run history) while the *source* is an API instead of a file. If the partner can't push events but *does* expose a "list changed since X" API, this is the tool.

Typical setup:

1. Create a Data Source of the REST type, pointing at the endpoint (authenticated via an **alias** from Module 2).
2. Define how the JSON maps to staging columns.
3. Load + transform on a schedule, using a **watermark** (e.g. `?since=last_run`) so each run fetches only what changed.

## Data Streams / Stream Connect

For data that changes constantly and must stay in sync, a **Data Stream** keeps the target current rather than doing a fresh full import each time:

- It reads from a source that exposes **changes** (a change feed, a queue, a CDC stream, or a REST endpoint with a cursor).
- New/changed items flow into GlidePort **continuously**, applying coalesce like a transform.
- Think of it as an import set that **never stops running**.

Use it when "the record is a few minutes stale" is a real problem — live agent positions, shared customer records.

> **Design note:** a stream is only as good as the source's change signal. If the source can't tell you *what changed*, you're back to periodic pulls — and a REST Data Source on a schedule is simpler.

## Other Sources You'll Meet

| Source | Notes |
| --- | --- |
| **JDBC** | Query a SQL database directly (via a MID server if on-prem) |
| **LDAP** | Import users/groups from a directory |
| **SOAP** | Older enterprise services |
| **OAuth/API Data Source** | REST JSON feeds (above) |

## Choosing, in One Table

| You need… | Reach for… |
| --- | --- |
| Instant reaction to an event | Webhook / inbound event |
| A value during a single transaction | Real-time API pull |
| Records to stay in sync continuously | Data Stream / Stream Connect |
| A JSON feed on a clock | REST-based Data Source + scheduler |
| A big periodic file | CSV File import set |

## Watermarks — Don't Re-Fetch Everything

For scheduled pulls, fetch only what changed. Keep the **last successful timestamp/offset** (a "watermark") in a system property or a row, and pass it to the API:

```
GET /v1/van/updates?since=2026-10-12T06:00:00Z
```

Update the watermark **only after** a clean transform. If a run fails, the next run re-fetches from the last good point — no gaps, no duplicates (coalesce handles the overlap).

## Lab: Stream the Van Locations

1. Take the REST-based Data Source pattern and point it at a JSON endpoint returning `{ "since": ..., "vans": [ … ] }`.
2. Map `vans[]` to a staging table, then transform with **coalesce on `van_id`** into an `u_van_location` table.
3. Add a **watermark**: pass the previous run's timestamp into the request; update it only after a successful transform.
4. Schedule it to run every 15 minutes; confirm each run only touches changed vans.
5. Decide whether this should really be a **Data Stream** instead, and write one sentence explaining your choice.

**Check your work:** repeated runs don't duplicate vans (coalesce), and each run requests only data since the last successful sync.

## Key Takeaways

- The refresh spectrum runs from **instant events** to **scheduled bulk files** — choose by need.
- **REST-based Data Sources** reuse the whole import pipeline with an API as the source.
- **Data Streams / Stream Connect** keep records in sync **near-continuously** from a change feed.
- Use a **watermark** to fetch only what changed since the last good run.
- Update the watermark **only after** a clean transform — that's what prevents gaps and duplicates.

## Best Practices

- Match **freshness to business value** — don't stream what a nightly file can serve.
- Never re-fetch everything if the source offers a "changed since" filter.
- Coalesce on a stable key so overlapping windows stay idempotent.
- Persist the watermark durably; losing it means a full re-sync or a data gap.
