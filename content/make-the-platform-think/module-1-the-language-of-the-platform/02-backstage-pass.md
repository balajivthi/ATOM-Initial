# Backstage Pass

**Story so far:** GlidePort's IT lead sees your JavaScript fundamentals and hands you the keys to the platform. Before writing real automation, you need to know *where* scripts run and how to *run your own* safely — without touching live processes.

This lesson covers the scripting workspace, server vs client, and the logging you'll use to debug.

## The Scripting Workspaces

| Editor | Where | Best for |
| --- | --- | --- |
| **Scripts Background** | `All → System Definition → Scripts Background` | Quick experiments, testing server-side logic |
| **Script Editor** | `All → System Definition → Script Editor` | Writing and saving snippets |
| **Script Includes** | `All → System Definition → Script Includes` | Reusable server-side classes |
| **Business Rules / Client Scripts** | Under their own modules | Automation scripts (later modules) |

> **Tip:** `Scripts Background` is your sandbox — code there runs on the server against real data, so be careful, but it's the perfect place to learn and test.

## Server vs Client

| | Server-side | Client-side |
| --- | --- | --- |
| **Runs on** | ServiceNow's servers | The user's browser |
| **Examples** | Business Rules, Script Includes, Scheduled Jobs | Client Scripts, UI Policies |
| **Data access** | Full (GlideRecord, GlideSystem) | Limited (form fields, glideForm) |
| **Why use it** | Business logic, security, heavy processing | Instant form feedback, UX |

Rule of thumb: put logic that must be **trustworthy** (validation, security, calculations) on the server, and only *experience* logic on the client.

## Writing and Running a Background Script

1. Open **All → System Definition → Scripts Background**.
2. Type a script in the **Script** pane:

```js
var name = 'GlidePort';
gs.info('Hello from ' + name + '! Scripts Background works.');
```

3. Click **Run script**.
4. Read the output in the **Output** pane and the logs under **System Logs → System Log**.

> The `gs` object is the **GlideSystem** — the server-side gateway for logging, user context, properties and more (next lesson).

## Logging Levels

`gs.info()` is the day-to-day choice. Use levels deliberately:

| Method | Use when |
| --- | --- |
| `gs.info(msg)` | Normal progress messages |
| `gs.warn(msg)` | Something unexpected but not fatal |
| `gs.error(msg)` | A failure worth investigating |
| `gs.debug(msg)` | Verbose debugging (only shows when debug is on) |

Log output appears under **System Logs → System Log** and **System Logs → Scripts**. Prefix messages (e.g. `[DeliveryApp]`) so they're easy to search for.

## Syntax Errors and Debugging

- **Red underlines** in the Scripts Background editor point at syntax errors before you run.
- Errors at runtime appear in the Output pane with a **line number** — read it.
- Wrap risky code in `try/catch` to control failure:

```js
try {
    // risky logic
    var agents = new GlideRecord('u_delivery_agents');
    agents.get('name', 'Ana');
    gs.info('Found agent: ' + agents.getValue('name'));
} catch (e) {
    gs.error('Delivery script failed: ' + e);
}
```

## Lab

1. Open **Scripts Background**.
2. Run a script that logs your name and the current user:
   ```js
   gs.info('Running as: ' + gs.getUserName());
   ```
3. Write a loop that logs numbers 1–5 using both `for` and `while`.
4. Deliberately introduce a syntax error, run it, and read the error output — then fix it.
5. Wrap a `try/catch` around `gs.getUserName()` and confirm the output still appears.

## Key Takeaways

- **Scripts Background** is your safe sandbox for server-side experiments.
- Server-side = trust and data; client-side = form experience.
- `gs.info/warn/error/debug` are your debugging toolkit.
- Read error output with line numbers and use `try/catch` for graceful failure.
- Prefix logs so you can find them in **System Logs**.
