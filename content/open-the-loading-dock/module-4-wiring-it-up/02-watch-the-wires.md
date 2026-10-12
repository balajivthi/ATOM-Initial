# Watch the Wires

**Story so far:** GlidePort now has dozens of wires running to partners and back. On a good day they're invisible. On a bad day — the partner changes their API, a token expires, a file arrives malformed — you need to *see* what's flowing. This lesson is integration operations: logs, errors, retries, and alerts.

## Integrations Fail Quietly

A broken UI shows a red box. A broken integration often shows **nothing** — the data just stops. That silence is the danger: orders don't get booked, and no one notices for a day. **Observability is not optional** for integrations.

## Where the Evidence Lives

| Layer | Where to look | Tells you |
| --- | --- | --- |
| **Outbound calls** | **Outbound HTTP Requests** (`sys_outbound_http_log`) | URL, method, status, body, timing |
| **REST Messages** | REST Message / method logs | Per-message call history |
| **Inbound events** | Your staging table + the API log | What partners sent, and when |
| **Import Sets** | Import Set Run history | Rows loaded / transformed / errored |
| **Flows** | Flow executions | Each step's inputs, outputs, result |
| **Scheduled jobs** | Scheduled job history | Did the batch run? Did it fail? |

When someone asks *"did the shipping update go through?"*, one of these has the answer.

## A Debugging Playbook

1. **Locate the wire** — outbound call, inbound event, or import?
2. **Find the last run** in the matching log/history.
3. **Read the status and body.** A `401` is auth; `404` is a wrong id; `500` is the partner; `429` is rate-limiting.
4. **Check the inputs.** For flows, the *step inputs* reveal empty pills or wrong ids.
5. **Reproduce** in a sandbox or with a test client.
6. **Fix, then verify** the next run is green.

| Symptom | Likely cause |
| --- | --- |
| Everything works, then stops at a timestamp | Token expired, or partner change |
| `401` suddenly | Credential rotated / token revoked |
| `429` | Too many calls — add backoff or reduce polling |
| Import rows loaded, none transformed | Transform map condition / coalesce |
| Flow ran but no data updated | Empty data pill or a swallowed Catch |

## Transient vs Permanent Failures

React differently — this distinction saves you from both noise and silence:

| | **Transient** | **Permanent** |
| --- | --- | --- |
| Examples | `429`, `5xx`, timeouts | `400`, `404`, bad payload |
| Response | **Retry** with backoff | **Don't retry** — alert and fix |
| Risk | Piling on a struggling partner | Retrying forever, hiding a real bug |

**Retry policy:** a few attempts, exponential backoff, honor `Retry-After`; then stop and raise a task.

## Handling and Alerting

Wrap every external call so a failure is *visible and owned*:

```
[ Try ]  call the partner API
[ Catch ]
   ├─ Log (level: error): "Shipping sync failed for {{number}}: {{error}}"
   ├─ Create Task: "Fix shipping integration" (assigned to: integration team)
   └─ (optional) Post to team channel
```

A failure should produce at least one of: a **log with detail**, an **assigned task**, or a **notification**. A silent Catch is the worst outcome.

## Guarding the Line: Health Checks

Proactive beats reactive:

- **Counters** — calls attempted vs succeeded per day; alert when the success rate drops.
- **Dead-letter table** — park failed payloads somewhere a human can replay them.
- **Heartbeats** — "the nightly import should have run by 07:00; if it hasn't, tell someone."
- **Synthetic checks** — a tiny periodic outbound call to confirm the partner is reachable.

## Lab: Find a Broken Wire

1. Make a deliberate outbound failure (point the shipping call at a bad URL).
2. Run it via a flow or Scheduled Job.
3. Open **Outbound HTTP Requests** and find the failed call; read the status/body.
4. Add a **Try/Catch** to the flow: log at error level and **create a task**.
5. Run again; confirm the task appears and the log line names the order.
6. Add a simple heartbeat: a scheduled job that errors if no successful run today.

**Check your work:** you can answer "what failed, when, and for which order" from the logs alone, and a human task is created on failure.

## Key Takeaways

- Integrations fail **quietly** — logs and alerts are how you notice.
- Evidence lives in the **outbound HTTP log, import run history, and flow executions**.
- Distinguish **transient** (`429`/`5xx` → retry) from **permanent** (`400`/`404` → alert) failures.
- Every external call should **log, alert, or recover** on failure — never swallow silently.
- Add **health signals**: success counters, dead-letter parking, heartbeats.

## Best Practices

- Log with identifying data (partner, order number, status code).
- Create an **assigned task** — logs are read by humans, tasks are *owned* by them.
- Cap retries with backoff; alert after the cap.
- Review integration health after every partner release — APIs change without asking you.
