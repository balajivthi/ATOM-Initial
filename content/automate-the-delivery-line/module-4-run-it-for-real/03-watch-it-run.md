# Watch It Run

**Story so far:** The flows are built and the tools are chosen. But automation you can't see is automation you can't trust. This lesson is the observability kit — executions, logs, debugging, and the settings that keep a live flow healthy — capped with the course's final lab.

## Every Run Is Recorded

When a flow fires, the platform writes a **flow execution** record (`sys_flow_context` and friends). To inspect one:

1. **Flow Designer → open the flow → Executions** (or the record's *Flow Executions* related list).
2. Click a run to see each step, its **inputs**, its **outputs**, and its **result**.
3. A red step marks where it failed — with the error message attached.

This is your first stop for *"why didn't the customer get the email?"*

## Reading an Execution

An execution shows, step by step:

| Column | What it tells you |
| --- | --- |
| **Step** | Which action/logic block ran |
| **State** | Completed / Skipped / Failed / Waiting |
| **Inputs** | The actual values that arrived (the data pills resolved) |
| **Outputs** | What the step produced |
| **Error** | The message if it failed |

A step showing `Skipped` usually means an **If** branch wasn't taken — that's normal and useful: it proves the logic chose the other path.

## Debugging a Broken Flow

A repeatable approach:

1. **Reproduce** — trigger the flow again (create the record, or use **Test**).
2. **Find the failed step** in the newest execution.
3. **Read its inputs.** Is a pill blank? Is it the wrong record? The input is almost always the culprit.
4. **Fix above the failure.** If a pill is empty, the *step that should have produced it* is where you look.
5. **Re-test** and confirm the state turns green.

| Symptom | Likely cause |
| --- | --- |
| Flow never runs | Not active, wrong trigger table, or a trigger condition filtered it out |
| Flow runs but emails blanks | A data pill resolves to an empty field |
| Flow aborts mid-way | An unhandled error — wrap it in Try/Catch (Module 3) |
| Runs twice | Run mode is *for each update* where you wanted *Once* |
| Step shows Skipped | An If branch chose the other path — check the condition |
| Approval never finishes | The wait has no timeout, or no approver was set |

## Test, Replay, and Roll Back

- **Test** runs the flow against a chosen record in a safe panel — no real side effects until you're satisfied.
- **Replay** is useful when you've fixed a bug and want to re-run the *same* triggering record. (Guard against duplicate side effects — the flow will run its actions again.)
- **Snapshot / version**: before big edits, save the flow so you can restore a known-good version. Keep a description of each change.

## Settings That Keep Flows Healthy

| Setting | Effect |
| --- | --- |
| **Active** | Off = dormant; On = live |
| **Run as** | The permissions the flow executes with (Module 2) |
| **Run trigger / mode** | How often a record flow fires (Module 2) |
| **Error handling** | Wrap risky steps in Try/Catch; decide whether one failure aborts the run |
| **Description & documentation** | Future-you's map of what the flow is meant to do |

## Operational Habits

- **Name flows and steps** like sentences (`Book the van`, not `Step 7`).
- **Stage** long flows so a failed run points to a chapter.
- **Alert on the important failures** — a task or notification, not just a log line.
- **Review executions** after a release to catch silent breakage.
- **Keep a description** of every custom action/subflow's inputs and outputs.

## Lab: The Delivery Automation (Capstone)

Bring the whole course together into one end-to-end flow — then prove it works.

**Build `Automate the Delivery Line`:**

```
Stage: Intake
  Trigger: Record → Created · Order & Tracking
  If ( Priority is Priority )  →  Call Subflow: Book Delivery Van (express)
  Else                         →  Call Subflow: Book Delivery Van (standard)

Stage: In Motion
  Update Record: status = scheduled
  Send Notification to customer: "Your order {{number}} is scheduled."
  Wait for condition ( status = delivered, timeout 3 days )
     ├─ met       → Update status = closed; Email a thank-you
     └─ timed out → Try: Get Van ETA (custom action)
                       └─ Catch → Create Task: "Chase overdue order {{number}}"

Stage: Wrap-up
  Log: "Delivery journey complete for {{number}}"
```

**Verify it:**

1. **Test** with a priority order and a standard order — confirm each takes its branch.
2. Create a real order and open its **Executions** — walk every step, and confirm the log line.
3. Force the timeout path (shorten it for the test) and confirm the overdue task is created and the error (if any) is caught.
4. Confirm the flow reads top-to-bottom as three named stages.

**Check your work:** a single, readable flow that books a van, schedules, waits, closes the order, and gracefully handles an overdue delivery — with every run visible in the execution log.

## Key Takeaways

- Every run is recorded as a **flow execution** — steps, inputs, outputs, and errors.
- **Debug from the failed step's inputs**; the missing value is usually upstream.
- **Test** before activating; **replay** after a fix (mind duplicate side effects).
- Health settings — **active, run-as, run mode, error handling** — are part of the design.
- Name, stage, document, and **alert on important failures**: observable automation is trustworthy automation.

## Course Wrap-Up

You began with Business Rules reacting to a single record. You now automate a **whole journey** — one trigger, named stages, forked branches, loops, waits, reusable blocks, and graceful failure handling — all visible and logged.

**Automation makes the platform run for you. Next in the GlidePort arc: opening that automation to the outside world — integrations that connect the Delivery App to partners and customers.**
