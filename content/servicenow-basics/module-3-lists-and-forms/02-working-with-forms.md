# Working with Forms

A **form** is the view used to create, read and edit a single record. Forms are what end users and agents interact with most, and configuring them well is a core admin skill.

## Opening a Form

- Click a record in any list to open its form.
- Or use the navigation shortcut: `incident.form` opens a blank incident form; clicking a specific record in a list opens that record's form.

## Anatomy of a Form

| Element | Purpose |
| --- | --- |
| **Form header** | Table name, record number, state and the **contextual app pill** |
| **Additional actions** | The hamburger (⋯) menu with Configure, Copy, Delete and more |
| **Sections** | Grouped fields (e.g. "Caller Information", "Assignment", "Task") |
| **Fields** | The columns of the record; some are mandatory (red asterisk) |
| **Related lists** | Other tables linked to this record (e.g. Work notes, Activity) |
| **Submit / Update** | Save the record |

## Configuring the Form Layout

Two configuration tools control how a form looks and behaves. Both are reached from the form itself.

### Option 1: Form Design

1. Open a record (for example, an incident).
2. Click the **Additional actions** (⋯) menu — or right-click anywhere on the form.
3. Choose **Configure → Form Design**.
4. In the designer you can:
   - **Reorder** fields by dragging them.
   - **Create new columns** / sections.
   - Move fields between sections and columns.
5. Click **Save**.
6. Return to the form and observe that the changes are applied immediately.

### Option 2: Configure Form Layout

1. Open a record.
2. Right-click (or **Additional actions → Configure → Form Layout**).
3. Use the two-pane editor: available fields on the left, current layout on the right.
4. Move fields between the panes to add/remove them from sections.
5. Click **Save**.

> **Form Design** is the newer, more visual editor; **Form Layout** is the classic two-pane editor. Both achieve the same goal — use whichever you prefer.

## Common Form Configuration Tasks

- **Make a field mandatory**: right-click the field → **Configuration → Dictionary**, and set **Mandatory** to true.
- **Change a field's order**: drag it in Form Design.
- **Hide a field** (admin only): use **UI Policies** or set the field's visibility in the Dictionary.
- **Show/hide based on values**: UI Policies react to field changes (e.g. show a "Resolution" section only when State = Resolved).

## Lab

1. Open `incident.list` and open any incident record.
2. Click **Additional actions → Configure → Form Design**.
3. Reorder two fields (for example, move **Caller** above **Category**).
4. Click **Save** and return to the form — the new order is visible.
5. Repeat with **Configure → Form Layout** to confirm the same reordering works there.
6. Try right-clicking a field and opening **Configuration → Dictionary** to inspect its properties.

## Key Takeaways

- Forms display a single record and are built from sections and fields.
- **Form Design** and **Configure Form Layout** both let admins rearrange fields without scripting.
- Configuration changes to a form apply immediately after saving.
- Field behaviour (mandatory, visibility) is controlled via the Dictionary and UI Policies.
