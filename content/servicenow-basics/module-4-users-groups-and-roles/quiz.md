# Quiz: Users, Groups & Roles

Answer these questions about users, groups and roles. Your score is saved, and reasoning is revealed after you submit.

1. In which table are user records stored?
   A. sys_group
   B. sys_user
   C. sys_user_role
   D. sys_audit
   CORRECT: B
   EXPLAIN: User records live in the `sys_user` table — open it with the `sys_user.list` shortcut.

2. A brand-new user who has no roles is called a(n):
   A. Admin
   B. ITIL user
   C. End user
   D. Approver
   CORRECT: C
   EXPLAIN: New users are end users: they can use the Service Portal but have very limited access to the back-end applications.

3. What is the recommended way to grant the ITIL role to several users?
   A. Add the role to each user one by one
   B. Add the role to a group, then add the users to that group
   C. Ask users to add the role themselves
   D. Set everyone as admin
   CORRECT: B
   EXPLAIN: Assign roles to groups and users to groups — permissions flow to all members automatically instead of being managed per person.

4. What does "Impersonate" let an admin do?
   A. Delete another user
   B. See the platform exactly as another user sees it
   C. Reset another user's password permanently
   D. Merge two user accounts
   CORRECT: B
   EXPLAIN: Impersonation is a testing tool — you view the platform with another user's permissions to verify access, then "End Impersonation".

5. Which role is the typical first role for support agents?
   A. admin
   B. ITIL
   C. approver_user
   D. snc_platform_editor
   CORRECT: B
   EXPLAIN: ITIL is the classic starter role that grants access to incidents, requests, problems and changes.
