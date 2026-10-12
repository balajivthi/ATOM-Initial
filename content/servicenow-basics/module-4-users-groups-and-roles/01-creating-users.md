# Creating Users

Users are the people who access your instance. Creating a user correctly — and understanding their default permissions — is one of the first admin tasks you learn.

## Where Users Live

User records are stored in the **User** table (`sys_user`). Open it with `sys_user.list`, or navigate via **All → Users → Users** (under User Administration).

## Creating a User

1. Open the User table list (`sys_user.list`).
2. Click **New**.
3. Fill in the key fields:
   - **User ID**: conventionally `firstname.lastname` (e.g. `john.smith`). This is the login ID.
   - **First name**, **Last name**.
   - **Email**: used for login, notifications and password resets.
4. Click **Submit**.
5. Open the newly created user and click **Set Password** (in the form's related actions).
6. In the pop-up, click **Generate** to create a random password, then **Save**.
7. Click the **copy** icon and store the password somewhere safe (you will need it to log in as this user).

## What Can a New User Do?

By default, a brand-new user has **no roles**. Such users are called **end users**:

- They can log in through the **Service Portal** (the user-facing web interface).
- They have very limited access to the back-end applications — no incident lists, no admin modules.
- Most platform functionality (lists, forms, modules) is gated by **roles**, which we add next.

### Test it yourself

1. Open a new **incognito/private browser window** and navigate to your instance.
2. Log in with the new user's **User ID** and the generated password.
3. ServiceNow redirects to a **password reset** page — set a password you will remember.
4. After logging in, observe how little the user can access compared to your admin account.

> **Security note:** `Set Password` is intended for admin-provided initial passwords or emergency resets. Self-service password reset is normally handled by the instance's password reset policy or SSO.

## Key Takeaways

- User records live in the `sys_user` table; the **User ID** is the login name.
- Use `firstname.lastname` as a consistent naming convention.
- **Set Password → Generate** creates a temporary password for a user.
- New users have **no roles** → they are **end users** with minimal access.
- Access is granted by adding roles (directly or via groups), covered next.
