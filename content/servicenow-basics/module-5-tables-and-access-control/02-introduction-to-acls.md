# Introduction to ACLs

**Access Control Rules (ACLs)** decide who can read, write, create or delete records in your instance. They are the platform's security backbone — and the reason a new user sees almost nothing until you grant them access.

## What is an ACL?

An ACL is a rule on a table (or field) that answers: **"Can this user perform this operation?"**

Each ACL has:

- **Type**: read, write, create or delete.
- **Table**: which table it protects.
- **Roles**: which roles are allowed.
- **Conditions**: an optional filter that must match for the rule to apply.
- **Script**: optional advanced logic returning true/false.

ACL records live in the **Access Control** table (`sys_security_acl`), reachable via **All → System Security → Access Control (ACL)**.

## How Access is Decided

1. When a user performs an action, the platform looks for ACLs on the table.
2. If a matching ACL allows the operation **and** the user meets its roles/conditions, access is granted.
3. If no ACL grants access, the operation is **denied by default**.

That default-deny behaviour is why a brand-new table with **"Create access control" unchecked** is invisible to everyone except admins — there are no ACLs granting access yet.

> Admins (users with the `admin` role) bypass ACL checks, which is why you can see everything but your test users cannot.

## The Day 5 Lab: Gating a Table

The training lab demonstrates the full flow:

### 1. Observe the denial

1. Log in as a **demo user** (an end user with no relevant roles).
2. Notice the new **Delivery App** table/application is **not visible** to them.

### 2. Grant access via roles and groups

As **admin**, assign roles to groups, and add users to those groups:

| Group | Role |
| --- | --- |
| Delivery Agents | `app_support_user` |
| Delivery Support Users | `app_support_user` |
| Delivery App Admins | `app_admin` |

Make sure different users are assigned to each group (see the *Creating Groups and Roles* lesson for how).

### 3. Verify access

1. Log out the demo user, close the tab, and log back in from a fresh incognito window.
2. The **Delivery App** table and application are now accessible.
3. The user's permissions now honour the ACLs — they can use what the roles allow and nothing more.

## Common ACL Patterns

| Pattern | Example |
| --- | --- |
| **Role-only** | Allow `app_support_user` to read the Order & Tracking table |
| **Owner-based** | Allow a user to update a record only when **Caller is (dynamic) Me** |
| **State-based** | Only allow editing when **State ≠ Closed** |
| **Field-level** | Hide the *Cost* field from non-managers |

## Reading an ACL Record

Open an existing ACL (e.g. on the Incident table) and notice:

- The **Type** (read/write/…) and **Table**.
- The **Requires role** field.
- The **Conditions** tab with a filter builder.
- The **Script** tab — where you can return `true`/`false` dynamically.

## Key Takeaways

- ACLs are **default-deny** rules controlling read/write/create/delete on tables and fields.
- **Roles + groups** are the usual mechanism for granting access at scale.
- A table created **without** Create access control is hidden from everyone but admins.
- `admin` role bypasses ACLs — test with impersonation to see real permissions.
- ACLs combine **roles**, **conditions** and optional **scripts** for fine-grained control.
