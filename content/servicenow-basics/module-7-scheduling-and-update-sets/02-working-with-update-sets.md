# Working with Update Sets

**Update sets** package the configuration changes you make on one instance so they can be moved to another (dev → test → production). When you created an update set in the UI Navigation lesson, you started capturing every change into it. This lesson shows how to export and import it.

## Why Update Sets?

Configuration lives on a specific instance. To promote it safely, you collect your changes into a portable unit and move it:

```
Dev instance  ── export XML ──►  file  ──── import ──►  Test/Prod instance
```

Update sets also give you a **rollback / review** point: you can preview exactly what will change before committing it.

> **Modern note:** ServiceNow is increasingly promoting **App Engine Studio + Source Control** (Git) for application development, but update sets remain the standard, universal mechanism for promoting customisations — especially in classic admin work.

## Capturing Configuration

Everything you do while an update set is **current** is tracked automatically:

1. Navigate to **All → System Update Sets → Local Update Sets** (or `sys_update_set.list`).
2. Open the update set you created earlier (e.g. **Training Updates**).
3. Confirm its **State** is **In Progress** and it is **Current**.
4. Any record you create or modify is now captured as an **update** in this update set.

> Rule of thumb: one update set per **feature or task** — don't bundle unrelated changes.

## Exporting an Update Set to XML

1. Open the update set record.
2. Change the **State** from **In Progress** to **Complete** and click **Save**.
   - Marking it complete closes it to new changes and enables the export options.
3. In the **Related Links**, click **Export XML**.
4. ServiceNow downloads a single **XML file** containing all the customisation captured in the update set.
5. Save the file somewhere you can retrieve it (email, shared drive, repo).

## Importing an Update Set on Another Instance

1. On the **target instance**, navigate to **All → System Update Sets → Retrieved Update Sets**.
2. Click **Import Update Set from XML**.
3. In the pop-up, select the downloaded XML file and click **Upload**.
4. A new **Retrieved Update Set** record appears with the same name.

## Preview and Commit

1. Open the retrieved update set record.
2. Click **Preview Update Set** — the platform checks whether the target instance is ready (missing plugins, conflicting fields) without applying anything.
3. Once preview completes, click **Commit Update Set**.
4. The changes are applied to the target instance and the update set state moves to **Committed**.

## Update Set States

| State | Meaning |
| --- | --- |
| **Draft** | Just created, capturing not yet started |
| **In Progress** | Current — capturing your changes |
| **Complete** | Done capturing; ready to export |
| **Committed** | Imported and applied on the target instance |

## Best Practices

- Name update sets descriptively (e.g. `Feature: Delivery App tables`).
- Keep one update set **current** at a time and switch back when a task is done.
- Always **Preview** before **Commit** on the target.
- Commit from the **source** update set is different from retrieved sets — track which updates are already promoted.
- Avoid editing records directly in production; use update sets or source control.

## Lab

1. Verify your update set from the UI Navigation lesson has **State = In Progress**.
2. Make a small change (e.g. add a column to the Delivery Agents table).
3. Open the update set, set **State = Complete**, and click **Export XML**.
4. On a second instance (or a fresh one), go to **Retrieved Update Sets → Import Update Set from XML**, upload the file.
5. **Preview** then **Commit**, and verify the column now exists on the target.

## Key Takeaways

- Update sets capture and transport configuration between instances as a single XML file.
- Capturing happens automatically while the update set is **current / In Progress**.
- Export from the source, import into **Retrieved Update Sets**, then **Preview → Commit** on the target.
- Follow best practices: descriptive names, one feature per set, and always preview before commit.
