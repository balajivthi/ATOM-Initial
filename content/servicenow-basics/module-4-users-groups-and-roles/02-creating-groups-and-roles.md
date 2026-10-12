# Creating Groups and Roles

**Groups** and **roles** are how ServiceNow grants access at scale. Instead of assigning permissions to every individual user, you assign **roles to groups** and add **users to groups**. Permissions then flow to members automatically.

## The Relationship

```
Roles (what you can do)   --assigned to-->   Groups
Groups (a team)           --contains-->      Users
So: a user's permissions = roles of their groups + their own direct roles
```

## What is a Role?

A **role** is a named set of permissions (the applications, modules and data a holder can access). Common examples:

| Role | Grants access to |
| --- | --- |
| **ITIL** | Working with incidents, requests, problems and changes |
| **admin** | Everything — full platform administration |
| **snc_platform_editor** | Developer access to build applications |
| **approver_user** | Approving catalog requests |

Roles are managed via **All → User Administration → Roles**, or `sys_user_role.list`.

## Creating a Group

1. Navigate to **All → User Administration → Groups** (or `sys_user_group.list`).
2. Click **New**.
3. Populate:
   - **Name**: e.g. `Training Group`
   - **Group email**: used for notifications and assignments
   - **Manager**: choose a user (for example, the user you created in the previous lesson)
4. Click **Submit**.

## Adding a Role to a Group

1. Search and open the newly created group.
2. On the **Roles** related list, click **Edit**.
3. Search for a role (e.g. **ITIL**) in the slush bucket, add it to the selected side, and click **Save**.
4. The role is now granted to the whole group.

## Adding Members to a Group

1. Open the group record again.
2. On the **Group Members** related list, click **Edit**.
3. Add the user(s) you want, then click **Save**.

### Verify it works

1. Open any user that was added as a group member and observe that **ITIL** now appears in their **Roles** related list (roles inherited from a group show up there).
2. Log in as that user (or impersonate them from your admin user menu) and re-run the earlier navigation exercise — they now have access to ITIL applications such as incidents.

## Inheritance Rules

- A role assigned to a group is granted to **all** group members.
- Users can hold roles **directly** and **via groups**; the effective permission set is the union.
- Removing a user from a group removes the group's roles from that user.
- **ITIL** is the classic starter role for agents; admins typically also need `admin` or specific application roles.

## Lab

1. Create a group named **Training Group** with yourself as Manager.
2. Add the **ITIL** role to the group.
3. Add the user from the previous lesson as a group member.
4. Impersonate that user and confirm they can now open the Incident application.

## Key Takeaways

- **Groups** collect users; **roles** carry permissions; roles on groups apply to all members.
- Grant permissions by role-to-group and group-to-user — never role-by-role per person.
- ITIL is the typical first role for support agents.
- Use **Impersonate** (from the user menu) to verify exactly what a user can see.
