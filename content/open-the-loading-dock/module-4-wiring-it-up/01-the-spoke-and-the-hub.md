# The Spoke and the Hub

**Story so far:** You can call out, authenticate properly, receive events, and batch-import files. So far every integration has been hand-built. But GlidePort isn't the first company to need "post a message to the team" or "create a Jira ticket" — the platform ships **prebuilt integrations** for exactly that. This lesson is about the hub and its spokes.

## The Hub and Spoke Idea

Think of a bicycle wheel:

- The **hub** is the platform's integration engine and action library.
- Every **spoke** is a prebuilt set of actions for one external system — Teams, Slack, Jira, Azure, Workday, and hundreds more.

Instead of writing REST calls yourself, you **drag a spoke action** into a flow and fill in the blanks. The vendor-specific details (endpoints, auth, retries) are handled by the spoke.

```
            ┌─────────────┐
   Teams ◀──│             │──▶ Slack
            │  Integration │
   Jira  ◀──│     Hub      │──▶ Workday
            │  (spokes)    │
   Custom ◀─│             │──▶ REST step
            └─────────────┘
```

## Using a Spoke Action in a Flow

The pattern is identical to any flow action (*Automate the Delivery Line*):

1. Open a flow in **Flow Designer**.
2. Click **+**, search for the system (e.g. **Microsoft Teams**).
3. Pick the action — e.g. **Post Message**.
4. Provide inputs: which channel, which message — using **data pills**.
5. Attach an **alias** for authentication (Module 2) so no secret is typed in.
6. Test, then activate.

```
[ Order at risk ] ─▶ [ Teams: Post Message ]
                        channel: #dispatch
                        message: "Order {{number}} is overdue — please chase."
```

No REST call authored, no auth configured by hand — the spoke did it.

## Spoke Action vs REST Step vs Hand-Built Call

| Approach | Effort | Control | When to use |
| --- | --- | --- | --- |
| **Spoke action** | Lowest (drag-and-drop) | Vendor-managed | A popular system already has a spoke |
| **REST step** (flow) | Low | Full | Any API, no code, built into a flow |
| **Custom action** | Medium | Full, reusable | A REST call you'll reuse; wraps the plumbing |
| **RESTMessageV2 in script** | Highest | Total | Edge cases, dynamic URLs, pre/post logic |

**Guideline:** reach for the **simplest** that fits — spoke → REST step → custom action → script. Don't hand-roll what a spoke already does.

## Licensing Reality

Spokes are a **licensed** capability (IntegrationHub). The practical implications:

- The base platform covers **scheduled jobs, scripted REST, outbound REST, import sets** — most GlidePort needs.
- **Spoke actions** require an IntegrationHub entitlement; many common spokes are included in bundles, others are premium.
- The **REST step** in Flow Designer is available without a spoke, so you can still build no-code integrations.

Know the difference before you promise a stakeholder "we'll just use the Teams spoke."

## Building Your Own Spoke (When It's Worth It)

If your organisation integrates the *same* custom system across many flows, a custom action (or a lightweight spoke) pays off: define the actions once, reuse them everywhere, version them centrally. For a one-off, a REST step is cheaper.

## The Payoff: A Common Language

Once GlidePort's integrations are a mix of spokes and custom actions, new automation becomes assembly:

```
Flow "Chase overdue order"
  ├─ Custom action: Get Van ETA
  ├─ Spoke action: Teams → Post Message
  └─ Custom action: Notify Customer
```

Everyone — developer or not — reads the flow and sees business steps, not HTTP minutiae.

## Lab: Put a Spoke in the Loop

1. In your delivery flow, add a notification step. Use a **spoke action** if one is available (Teams/Slack/email). If you have **no spoke**, add a **REST step** that posts to the request sandbox — `POST https://httpbin.org/post` with a JSON body like `{ "order": "…", "agent": "…" }` — which echoes exactly what you sent (see [Lab Setup](/lab-setup)).
2. Provide its inputs with **data pills** (order number, agent).
3. Attach an **alias** for authentication.
4. Test the flow; confirm the step fires with a **`200`** in the execution log — and, for httpbin, that the echoed body contains your order number.
5. Write one sentence: why did you choose a spoke, REST step, or custom action here?

**Check your work:** the flow posts to the team (or calls the API) with no secret in the flow and no hand-written auth.

## Key Takeaways

- The platform's integration engine is a **hub** with prebuilt **spokes** for popular systems.
- Spoke actions are drag-and-drop blocks — vendor details handled for you.
- Choose the **simplest fit**: spoke → REST step → custom action → script.
- Spokes are **licensed**; REST steps and core integration features are not.
- Build a custom spoke/action only when you'll **reuse** it across flows.

## Best Practices

- Check for a **spoke** before writing any REST call to a common system.
- Always authenticate spokes and REST steps via **aliases**, never inline secrets.
- Wrap spoke/REST steps in **Try/Catch** — external systems fail (next lesson).
- Document which integrations are **licensed spokes** vs base-platform, so nobody is surprised.
