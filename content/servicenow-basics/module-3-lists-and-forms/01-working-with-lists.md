# Working with Lists

A **list** is the grid view of a table — many records at once, filterable and sortable. Understanding lists is the foundation of working in ServiceNow, because almost every admin task starts with "open the list".

## Opening a List

Open any table's list from the filter navigator:

1. Click **All** and find the application (e.g. **Incidents**).
2. Click the module that shows a list (for example **Incidents → All**).
3. Or type a shortcut such as `incident.list` into the filter navigator.

## Anatomy of a List

| Element | Purpose |
| --- | --- |
| **Breadcrumbs** | Shows where you are in the application tree |
| **Search / Filter bar** | Type to find records within the current list |
| **Column headers** | Click to sort; drag to reorder columns |
| **Checkboxes** | Select records for bulk actions |
| **Show/Hide Filter** | Toggle the advanced filter panel (conditions) |
| **List Controls** | Wrench/gear menu with filters, columns, export and more |
| **Pagination** | Page through records at the bottom |

## Filtering with Conditions

Lists show a subset of records based on **filter conditions**. The Day 1–3 training focused on this exact workflow:

### Run a quick filter

1. Open a list, e.g. `incident.list`.
2. Click **Show/Hide Filter** (top-left) to reveal the filter conditions panel.
3. Start with a condition like **Active is true** (the default for many tables).
4. Click **AND** to add another condition.
5. Pick the field, operator and value. For example:
   - Field: **Caller**
   - Operator: **is (dynamic)**
   - Value: **Me**
   
   The **is (dynamic)** operator is special — it resolves at runtime, so *Me* means "the user viewing the list". Any user who runs this filter automatically sees their own records.
6. Click **Run** to see the results.

### Save a filter for everyone

1. With your conditions set, click **Show/Hide Filter** and then click **Save**.
2. Choose **Everyone** so all users on the platform can see it.
3. Give the filter a name, e.g. **My Opened Incidents**, and click **Save** again.
4. Open the list again, click **List Controls** (the wrench icon), and choose **Filters** to see the saved filter.

> **Note:** Saved filters are visible to everyone on the platform, so use a clear, descriptive name.

## Personalising Columns

You can change which columns appear and their order without touching the configuration:

1. From the list, right-click a column header (or use **List Controls → Configure → List Layout**).
2. Add/remove columns from the layout editor.
3. Save — your personal column layout is remembered for your account.

## Sorting and Bulk Actions

- Click any column header to sort ascending, then descending.
- Tick the checkboxes of records, then use the action buttons (e.g. **Edit**, **Delete**, **Export**) to act on the selection.

## Lab

1. Open `incident.list`.
2. Click **Show/Hide Filter** and add: **Caller is (dynamic) Me**.
3. Click **Run** and confirm you see only incidents where you are the caller.
4. Save the filter as **My Opened Incidents** for **Everyone**.
5. Open **List Controls → Filters** and confirm the filter appears.

## Key Takeaways

- Lists are the table grid view; filters control which records show.
- **Conditions** combine fields, operators and values; AND/OR chain them together.
- **is (dynamic) Me** resolves per-user at runtime — perfect for personal lists.
- Saved filters (especially shared ones) are managed under **List Controls → Filters**.
- Column layout, sorting and bulk actions are personal, per-user preferences.
