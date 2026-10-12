# How the Platform Functions

ServiceNow is not just an application — it is a **platform** you configure and extend. To use it well, you need to understand the mental model behind it: **everything is data on a table, and applications are just layers of configuration over that data.**

## The Core Mental Model

At its heart, the Now Platform is a **database with a configuration layer**:

```
Tables (like spreadsheet sheets)
   └── Records (rows) — each record has fields (columns)
          └── Applications group related tables, forms, lists, workflows
```

Almost everything you "build" in ServiceNow is really a row in a table, a configured form/list, or a workflow — not compiled code.

### Tables

- A **table** stores records of the same type. For example, the **Incident** table stores every incident record.
- Tables inherit from each other (a **class hierarchy**). The base table is `sys_db_object`, and most business tables descend from the **Task** table — that's why Incident, Change, Problem and Request all share fields like *Short description* and *State*.
- Table names are lowercase and underscore-separated, e.g. `incident`, `sys_user`, `cmdb_ci`.

### Records and Fields

- Each row in a table is a **record**.
- Each **field** (column) has a type: string, integer, date/time, choice list, reference to another table, and so on.
- **Reference fields** are what make the platform relational — e.g. an Incident's *Caller* field references a record in the `sys_user` table.

### Forms and Lists

- A **form** is one record's view for creating and editing.
- A **list** is a table's data grid showing many records at once with filtering and sorting.

## The Layers of the Platform

| Layer | What it contains | Who works here |
| --- | --- | --- |
| **User experience** | Portals, workspaces, mobile apps, Next Experience UI | End users |
| **Application layer** | Forms, lists, workflows (Flow/Workflow), record producers, virtual agents | Admins, developers |
| **Process layer** | Business rules, approvals, notifications, SLAs, assignment rules | Admins, developers |
| **Data layer** | Tables, records, relationships, import sets | Everyone |
| **Security layer** | Users, groups, roles, ACLs | Admins |

## How Configuration Works

Most platform behaviour is **configuration** rather than code:

- **Fields & forms** — add fields, reorder sections, make fields mandatory.
- **Business rules** — run server-side logic automatically when a record is inserted/updated/deleted.
- **Client scripts & UI policies** — react to user actions on the form (show/hide fields, validate input).
- **Flows & Workflows** — orchestrate multi-step processes (create a record, wait for approval, send an email).
- **Notifications** — email/slack/etc. triggered by events such as record insertion.
- **ACLs** — control who can read/write/delete records.

When configuration is not enough, developers extend it with **client-side and server-side scripts**, **REST/SOAP APIs**, and **AI Agents**.

## The Platform's Key Shared Services

- **ServiceNow Store / App Engine Studio** — build and distribute applications.
- **Flow Designer** — modern, drag-and-drop automation (replacing legacy Workflow).
- **Virtual Agent / AI Agents** — conversational self-service.
- **Update Sets / Source Control** — package and move your customisations between instances.
- **Service Portal / Experience Builder** — the web front end for end users.

## Roles on the Platform

| Role | Typical activities |
| --- | --- |
| **End user** | Log in to the portal, raise requests/incidents, track progress |
| **ITIL user** | Work on incidents, requests and changes via forms/lists |
| **Admin** | Configure the platform: users, groups, forms, workflows, ACLs |
| **Developer** | Script, build integrations, create custom applications |

## Summary

- Everything in ServiceNow is **data on tables**, wrapped in configured forms, lists and workflows.
- The platform is organised in layers: experience → application → process → data → security.
- Most work is **configuration**; scripting and APIs handle the rest.
- Understanding tables and records first makes every later lesson (ACLs, imports, notifications) much easier.
