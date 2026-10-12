# The Platform Toolbox

**Story so far:** You can run scripts. Now you need the platform's tools *inside* your scripts — who's running, what's today, how to log, how to look up a value. That's the **GlideSystem** (`gs`).

`gs` is available in **every server-side script**. It's the Swiss-army knife of the Now Platform.

## What is GlideSystem?

**GlideSystem** (accessed as the `gs` object) gives server-side scripts:

- **User context** — who is running the script.
- **Logging** — info, warn, error, debug.
- **System properties** — platform settings.
- **Environment info** — time, date, language.
- **Actions** — record updates, event firing, URL generation.

## The Methods You'll Use Most

| Method | What it does |
| --- | --- |
| `gs.getUserName()` | Login of the current user |
| `gs.getUserID()` | Sys ID of the current user |
| `gs.info(msg)` / `gs.warn` / `gs.error` | Write to the system log |
| `gs.getProperty(name)` | Read a system property |
| `gs.setProperty(name, value)` | Write a system property |
| `gs.nowDateTime()` | Current date/time in the instance timezone |
| `gs.getUrl()` | Current page URL |
| `gs.addInfoMessage(msg)` | Show a message to the user |

## User Context

Every server script runs **as a user**. Use the context instead of hardcoding names:

```js
gs.info('Running as: ' + gs.getUserName());

if (gs.hasRole('admin')) {
    gs.info('This user is an admin.');
}

// Who is the current user, safely
var userId = gs.getUserID();
gs.info('User sys_id: ' + userId);
```

> This is how GlidePort personalises behaviour — e.g. a Business Rule that records *who* closed an order.

## System Properties

System properties are instance-wide settings stored as name/value pairs. They keep magic numbers out of your scripts:

```js
// Read
var minWeight = gs.getProperty('glideport.min_delivery_weight', 0);

// Write (rare — and it persists!)
gs.setProperty('glideport.urgent_delay_hours', 2);
```

- `gs.getProperty(name, default)` returns the default if the property is missing.
- Naming convention: `appname.property_name`.
- Prefer system properties over hardcoded values — they're configurable without code changes.

## Dates and Times

```js
var now = gs.nowDateTime();          // e.g. 2026-08-11 18:30:00
var date = gs.nowDate();             // e.g. 2026-08-11

gs.info('Today is ' + date);
gs.info('Right now ' + now);
```

Dates in Glide scripts are usually handled with the **GlideDateTime** class (covered with GlideRecord, where you'll set due dates on orders).

## Events and Messages

Flows and notifications often run on **events**. You can fire one from a script:

```js
gs.eventQueue('glideport.order.ready', current, current.number, 'URGENT');
```

And surface messages to the user on the portal:

```js
gs.addInfoMessage('Your delivery order was created.');
```

## Lab: A GlidePort Welcome Script

1. Open **Scripts Background**.
2. Log the current user's name and ID:
   ```js
   gs.info('User: ' + gs.getUserName() + ' (sys_id: ' + gs.getUserID() + ')');
   ```
3. Read a property with a default: `gs.getProperty('glideport.fleet_name', 'GlidePort Fleet')`.
4. Log today's date using `gs.nowDate()`.
5. Write a `try/catch` that logs "Script complete" via `gs.info` after all steps.

## Key Takeaways

- `gs` (GlideSystem) is available in every server-side script.
- Use user context (`gs.getUserName()`) instead of hardcoding.
- Keep settings in **system properties**, read with `gs.getProperty`.
- `gs.nowDateTime()` / `gs.nowDate()` for time.
- Fire events with `gs.eventQueue` to trigger flows/notifications.
