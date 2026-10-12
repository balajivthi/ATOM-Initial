# Getting Started with Virtual Agent

**Virtual Agent** is ServiceNow's conversational chatbot: it lets end users "chat" with the platform to get answers and complete tasks — resetting a password, checking a request, or ordering an item — without opening tickets or calling support.

## What is Virtual Agent?

- A **conversational self-service** channel on the Service Portal (and configurable on Slack, Teams, etc.).
- Built from **topics** — individual conversations the bot can hold.
- Uses the **Virtual Agent Designer** (under **Conversational Interfaces**) to author topics visually.
- Powered by **Natural Language Understanding (NLU)** and, on newer instances, **generative AI (Now Assist)** so users can type naturally rather than click menus.

> **Up to date:** ServiceNow is evolving from scripted Virtual Agent topics toward **AI Agents** (built in **AI Agent Studio**) that reason with LLMs. Virtual Agent topics remain the practical, lower-cost way to build deterministic conversations — and are exactly what this course's integration lesson uses.

## Key Concepts

| Term | What it is |
| --- | --- |
| **Topic** | A single conversation ("Ask ChatGPT", "Reset Password") |
| **Topic block** | A step in the conversation (message, question, action, condition) |
| **User input** | A question the bot asks; answers become variables |
| **Condition** | Routes the conversation based on the answer (valid vs invalid) |
| **Action** | Something the bot does (call a Flow/Action, create a record, call an API) |
| **Assistant** | A bot "persona" that collects topics for end users |

## Creating a Topic

1. Navigate to **All → Conversational Interfaces → Virtual Agent → Virtual Agent Designer**.
2. Click **Create** and choose **Topic**.
3. Name it (e.g. **Ask ChatGPT**) and save.
4. The canvas opens with a starting **Entry** point.

## Building the Conversation

Drag topic blocks onto the canvas and connect them:

1. **User Question** — ask the user for input, e.g. *"What would you like to ask?"* (answer stored in a variable like `prompt`).
2. **Condition** — check whether the answer is valid:
   - *Valid Question condition* — e.g. answer is not empty.
   - *End Conversation condition* — e.g. answer is empty → show a goodbye message.
3. **Action utility** — call an **Action** (e.g. the Flow Designer action `askChatGPT`) passing the user's `prompt`.
4. **Message** — show the bot's response (the action output) to the user.

## Testing the Topic

1. Click **Test** in the Designer to preview the conversation in a chat pane.
2. Or open the **Service Portal** and start a chat with your assistant, then type something that triggers the topic.

## Publishing Topics

- Topics are available to users after the containing **assistant** is **published**.
- Use **Now Assist / NLU** so users' natural phrasing matches the right topic.
- Track performance under **Virtual Agent → Analytics** (conversation completion, escalation to live agent).

## Key Takeaways

- Virtual Agent is the conversational self-service layer built from **topics**.
- Topics are authored visually in the **Virtual Agent Designer** with question, condition, action and message blocks.
- Actions let a topic call out to **Flows, APIs or Scripts** — that's how it becomes truly useful.
- Always **test** the topic and **publish** the assistant before end users can see it.
