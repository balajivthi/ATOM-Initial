# Scheduling Data Imports

The data source and transform map you built in the previous module can run **on a schedule**, so new data arriving in a file is automatically loaded and transformed without anyone clicking a button.

## Why Schedule Imports?

- External systems send data files on a cadence (daily, hourly).
- Scheduling removes manual effort and human error.
- Combined with transform maps, scheduled imports keep business tables current automatically.

## The Scheduling Mechanism

A **Scheduled Import** record wraps a **Data Source** and executes it on a trigger:

| Setting | Purpose |
| --- | --- |
| **Name** | e.g. `Schedule Agent data import` |
| **Data Source** | Which data source (and its transform map) to run |
| **Run** | Run once (at a specific time) or on a repeating schedule |
| **Timing** | Start time / repeat interval |

## Creating a Scheduled Import

1. Navigate to **All → System Import Sets → Administration → Scheduled Imports** (or `sys_trigger` with a scheduled import record type).
2. Click **New**.
3. Configure:
   - **Name**: e.g. `Schedule Agent data import`.
   - **Data Source**: search for and select the **Delivery Agents data source** you created earlier.
   - **Run**: choose **Run once**.
   - **Timing**: set the start time about **2 minutes from now**.
4. Click **Submit** and save.

## Preparing New Data

For the import to pick up fresh data, update the attachment on the data source:

1. Open the data source.
2. **Remove** the old attachment.
3. **Attach** the new data file (e.g. a second Excel with additional agent rows).

> The scheduled job loads whatever file is currently attached and runs the transform map against it.

## Watching It Fire

1. Wait the 2 minutes until the scheduled time passes.
2. Open the **Delivery Agents** table list (`u_delivery_agents.list` or your custom table name).
3. Observe that the schedule **automatically transformed** the new data — new records appear without you running anything manually.
4. (Optional) Check the data source's **Import Set** related list to see the run.

## Scheduling Notes

- For true recurring loads, choose **Run on demand / repeating** and pick a frequency (daily/weekly/hourly).
- Monitor **Import Set rows** for errors after each scheduled run.
- Consider a **Script** or **Flow** trigger for more advanced import automation (e.g. watching a shared drive).

## Lab

1. Attach a new Excel file to the **Delivery Agents data source**.
2. Create a scheduled import named **Schedule Agent data import**, pointing at the data source, run **once** at 2 minutes from now.
3. Wait, then open the Delivery Agents list and confirm the new rows were auto-imported.

## Key Takeaways

- **Scheduled Imports** run a data source (and its transform) automatically on a timer.
- Swap the attachment on the data source to feed it new data each run.
- Recurring schedules keep tables current with minimal maintenance.
- Always review import set results after a run for errors.
