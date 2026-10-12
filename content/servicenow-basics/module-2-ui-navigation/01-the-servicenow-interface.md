# The ServiceNow Interface

Before you can configure anything, you need to be able to move around the platform confidently. This lesson tours the main interface and teaches the navigation tricks that admins use every day.

## The Parts of the Interface

Modern ServiceNow instances run the **Next Experience UI**, which unifies the classic environment and workspaces under one global navigation header.

### The Banner Frame (Global Header)

The bar at the top of every page is called the **banner frame**. It is where most navigation happens:

| Element | Purpose |
| --- | --- |
| **Logo / banner** | Click to return to the home/landing page |
| **All menu** | The main menu of every application and module on the platform |
| **Global search** | Search across records, tables, people and articles |
| **Notifications** | Bell icon for alerts about your records and approvals |
| **User menu** | Your avatar, profile, impersonation, preferences and logout |

### The All Menu

Click **All** (top-left, next to the logo) to open the **filter navigator** overlay. This is your map of the instance — every application and module you have access to appears here.

The All menu includes quick panels you can pin:

- **Favorites** — shortcuts to pages you star for fast access.
- **History** — pages you have visited recently.
- **Workspaces** — configurable agent workspaces (if enabled for your role).
- **Admin** — admin-only capabilities.

You can pin the All menu so it becomes a persistent sidebar instead of an overlay.

### The Filter Navigator

Inside the **All** menu (or as a pinned left panel), the **filter navigator** lists applications and modules in a tree. Each entry is a **module** — a saved list, form or report. To reach a module, click its name in the navigator.

## Navigation Shortcuts

The fastest way to move around as an admin is typing a **table navigation shortcut** directly into the filter navigator.

| Shortcut | Opens |
| --- | --- |
| `incident.list` | The list view of the Incident table |
| `incident.form` | A new (empty) incident record form |
| `sys_user.list` | The list of user records |
| `sys_user_group.list` | The list of groups |

> **Trick:** append `.LIST` in **capital letters** to open the list in a **new browser tab**, and `.FORM` (capital) to open a new-record form in a new tab. Example: `incident.LIST`.

Shortcut syntax is simple: `tablename.list` or `tablename.form`. You type it in the filter navigator search box and press Enter.

## Your First Lab

Follow these steps on your developer instance to get comfortable with navigation:

1. Log in to your instance (e.g. `https://dev12345.service-now.com`).
2. Click **All** on the banner frame and observe the filter navigator tree.
3. Type `incident.list` and press Enter — the **Incident** list opens.
4. In the filter navigator, type `incident.form` and press Enter — a blank incident form opens.
5. Use the **browser back** button or the breadcrumbs to return to the list.
6. Type `sys_user.list` and open the User table list.
7. Try `incident.LIST` (capital) and notice the list opens in a new tab.

### Lab Setup: Create an Update Set

Later lessons capture configuration in **update sets** so it can be moved between instances. Create one now (this is a prerequisite used by later labs):

1. In the filter navigator, go to **System Update Sets → Local Update Sets**.
2. Click **New**.
3. Give it a name, e.g. `Training Updates`, then click **Submit**.
4. From the form, click **Make Current** so this update set captures everything you do.

> Full update set mechanics are covered in the *Scheduling & Update Sets* module — for now you just need one in place.

## Key Takeaways

- Navigation happens from the **banner frame** and the **All menu / filter navigator**.
- Modules are saved lists, forms or reports inside the navigator.
- `tablename.list` and `tablename.form` shortcuts open lists and new-record forms instantly.
- Capital `.LIST` / `.FORM` open the destination in a new browser tab.
- Create an update set early so your lab configuration is captured for reuse.
