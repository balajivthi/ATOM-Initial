# Build a Catalog Item

**Story so far:** GlidePort's customers phone in to report damaged, missing, or late deliveries — every call ties up an agent. The team decides to let customers help themselves: a self-service form in the portal where they can report a delivery issue and watch it flow straight into the Delivery App. That's the **Service Catalog**.

## What Is the Service Catalog?

The **Service Catalog** is the storefront of a ServiceNow instance — a set of **Catalog Items** (things a user can request) organized into **Categories**, presented in the Service Portal.

A catalog item is a form with **Variables** (the questions the requester answers). Submitting the item can create a **Record Producer** record, open a **Request**, or trigger a **Flow**.

## Variables — the questions you ask

Every catalog item needs variables. Each variable is a form field the requester fills in:

| Variable type | Example for GlidePort |
| --- | --- |
| **Single Line Text** | Tracking code, name |
| **Multi-Line Text** | Details of the issue |
| **Choice** (dropdown/radio) | Issue type: damaged / missing / late |
| **Reference** | Look up the delivery order record |
| **Checkbox** | "Include a photo" |
| **Date / Date Time** | When the issue happened |

Variables have a **name** (used in scripts — we'll prefix references as `variable_<name>`) and a **label** (what the requester sees). Labels are friendly; names are technical.

## Lab: "Report a Delivery Issue"

Build a catalog item that feeds the Delivery App.

1. **All → Service Catalog → Catalog Definitions → Maintain Items → New** (class `Catalog Item`).
2. **Name:** `Report a Delivery Issue`
   - **Catalog:** GlidePort Service Catalog (create it if missing, category: Delivery Support)
   - **Short description:** `Tell us about a damaged, missing, or late delivery.`
   - **Price:** 0.00 — this is support, not a purchase.
3. Add variables to the **Variables** related list:

   | Name | Label | Type | Extra |
   | --- | --- | --- | --- |
   | `order_number` | Order Number | Reference → Order & Tracking (`u_order_tracking`) | Required |
   | `issue_type` | Issue Type | Choice | damaged / missing / late |
   | `details` | Describe the Issue | Multi-line text | Required |
   | `include_photo` | Include a Photo | Checkbox | — |
4. **Update**, then preview it.

## Test It

- Open the item in the **Service Portal**: `https://<instance>.service-now.com/now/nav/ui/classic/params/target/sp...` (or use the portal's home, search "Report a Delivery Issue").
- Order it as a customer would: pick an order, choose an issue type, type details, **Order Now**.
- A **Request** is created; if you wire a Record Producer, the issue can become a record on your delivery table.

## Record Producer vs Catalog Item

| | **Catalog Item** | **Record Producer** |
| --- | --- | --- |
| What the user sees | A requestable item | A requestable item |
| What it does | Creates a Request | Creates a record on a table (and/or a Request) |
| Best for | Orders, requests, purchases | Direct data entry with validation |

A **Record Producer** is your bridge from "customer filled a form" to "a row appeared in the Delivery App."

## Best Practices

- Every item lives in a **Catalog** under a **Category** — don't scatter items.
- Give variables clear names and labels; a label like "Where did you last see it?" beats "Location".
- Keep forms short — every extra question drops completion rates.
- Enforce required variables, then let scripts handle the clever stuff (next lesson).

## Key Takeaways

- The catalog is the self-service storefront; items ask questions via **variables**.
- Variables come in many types — pick the one that matches the answer.
- Submitting can create a Request (Catalog Item) or a record (Record Producer).
- A good catalog item is short, well-named, and tested in the Service Portal.
