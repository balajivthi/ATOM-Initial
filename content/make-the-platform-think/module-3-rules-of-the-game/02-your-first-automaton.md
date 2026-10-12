# Your First Automaton

**Story so far:** GlidePort approved your rule design. Now you'll build real automation for the Delivery App: default a status on insert, notify on status change, and keep a history trail — all with Business Rules you write and test in the UI.

## Building Rule #1: Default Status on Insert

Goal: every new order starts as `new`.

1. Go to **All → System Definition → Business Rules** (or `sys_script.list`).
2. Click **New**.
3. Configure:
   - **Name:** `Default order status`
   - **Table:** `u_order_tracking` (Order & Tracking)
   - **When to run:** **Before** · **Insert**
   - **Order:** 100
4. Script:
   ```js
   (function executeRule(current, previous) {
       if (!current.getValue('status')) {
           current.setValue('status', 'new');
       }
   })(current, previous);
   ```
5. Click **Submit**.

**Test:** create a new order with no status → it saves with `new`.

## Building Rule #2: React to a Status Change

Goal: when an order's status changes, log it and fire an event.

1. Create a new Business Rule.
   - **Name:** `Log order status change`
   - **Table:** `u_order_tracking`
   - **When to run:** **After** · **Update**
   - **Order:** 100
2. Script:
   ```js
   (function executeRule(current, previous) {
       if (previous && current.getValue('status') !== previous.getValue('status')) {
           gs.info('[DeliveryApp] Order ' + current.getValue('number') +
                   ' changed: ' + previous.getValue('status') +
                   ' → ' + current.getValue('status'));
           gs.eventQueue('glideport.order.status_change', current, current.number);
       }
   })(current, previous);
   ```
3. Submit, then open an order and change its status — check **System Logs** for your message.

## Building Rule #3: Guard Against Bad Data (Before)

Goal: prevent orders being marked `delivered` with no delivery date.

1. New Business Rule.
   - **Name:** `Require delivery date when delivered`
   - **Table:** `u_order_tracking`
   - **When to run:** **Before** · **Insert**, **Update**
2. Script:
   ```js
   (function executeRule(current, previous) {
       if (current.getValue('status') === 'delivered' &&
           !current.getValue('delivery_date')) {
           gs.addErrorMessage('Set a delivery date before marking this order delivered.');
           current.setAbortAction(true);      // stop the save
       }
   })(current, previous);
   ```
3. Submit. Try saving an order as `delivered` without a date — the save is blocked with your message.

## Testing Rules Safely

- **Impersonate** a regular user to see exactly what end users experience.
- **Audit**: Business Rules you create are captured in the current **update set** — check **System Update Sets → Local Update Sets**.
- Watch **System Logs → System Log** for your `[DeliveryApp]` messages.

## Where Rules Live in Your Update Set

Every rule you create is an **update** in your current update set, so it can be moved to test/prod later:

1. Open **System Update Sets → Local Update Sets**.
2. Open your training update set.
3. You'll see your three Business Rules listed under **Update**.

## Lab: The GlidePort Automation Pack

1. Create `Default order status` (before insert) → verify.
2. Create `Log order status change` (after update) → change a status, check the log.
3. Create `Require delivery date when delivered` (before insert/update) → verify the abort works.
4. Confirm all three appear in your current update set.

## Key Takeaways

- Business Rules are configured in the UI: name, table, when-to-run, order, script.
- **Before** rules can set defaults and block saves with `setAbortAction(true)`.
- **After** rules fire events and log — never abort.
- Use `previous` to react only to real changes.
- Rules are captured in your update set for promotion.
