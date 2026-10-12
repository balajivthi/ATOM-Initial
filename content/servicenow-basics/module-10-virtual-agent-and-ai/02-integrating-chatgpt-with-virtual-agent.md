# Integrating ChatGPT with Virtual Agent

This lesson builds a real integration: a user asks a Virtual Agent topic a question, and it sends that question to **OpenAI** and displays the AI's answer. It ties together **REST messages**, **Script Includes**, **Flow Designer Actions** and a **Virtual Agent topic**.

## Architecture

```
User in Service Portal chat
   └── Virtual Agent topic "Ask ChatGPT"
          └── Flow Designer Action (askChatGPT)
                 └── Script Include (ChatGPTOpenAI)
                        └── REST Message (ChatGPT)  ──► OpenAI API
                                                          └── answer back up the chain
```

> **No API key? You can still finish this lab.**
> - **Mock the model (no key, no signup).** Build the *exact same* chain but point the REST Message at `https://httpbin.org/post` — it echoes the JSON you send, so you can prove the whole **REST → Script Include → Action → Topic** plumbing works, then swap in OpenAI when you have a key. For this route, have the Script Include read `body.json.prompt` instead of `choices[0].message.content`.
> - **Free model tiers.** [Groq](https://groq.com) and [OpenRouter](https://openrouter.ai) hand out free API keys and speak the same OpenAI-compatible `/chat/completions` shape — only the endpoint URL and key change.
> - **A local model (e.g. Ollama) will not work here:** a cloud PDI cannot reach `localhost` on your laptop (you'd need a MID server or a public tunnel).

## Step 1: Get an OpenAI API Key

1. Sign up at [platform.openai.com](https://platform.openai.com).
2. Log in and go to **Users → API Keys**.
3. Click **Create new secret key**, give it a name, and **copy + save** it securely (it is shown only once).
4. (Optional) Add a small credit balance if your account has no trial credits.

> Keep the key secret — never share it or check it into source control. Store it as an environment/system property in production.

## Step 2: Create a REST Message

1. In ServiceNow, navigate to **All → System Web Services → Outbound → REST Message**.
2. Click **New**.
   - **Name**: `ChatGPT`.
   - **Endpoint**: `https://api.openai.com/v1/chat/completions`.
3. Click **Submit**.

> **Up to date:** Use the **chat completions** endpoint. The old `/v1/completions` endpoint is **legacy** and not supported by current models (gpt-4o family). Use the `messages` array format below.

### Configure the HTTP Method

1. On the **HTTP Methods** related list, click **New**.
2. Set **HTTP method** = **POST**.
3. In the **HTTP Request** section, add the request headers:
   - **Authorization**: `Bearer <your-api-key>`.
   - **Content-Type**: `application/json`.
4. Add the request body as JSON (variable substitution inserts values at runtime):
   ```json
   {
     "model": "gpt-4o-mini",
     "temperature": 0.5,
     "messages": [
       { "role": "user", "content": "${prompt}" }
     ]
   }
   ```
5. Click **Submit**.

### Auto-generate Variables and Test

1. Open the REST message and click **Auto-generate variables**.
2. Set **Test Values** for the generated variables (e.g. `prompt` = *"What is ServiceNow?"*, `model` = `gpt-4o-mini`, `temperature` = `0.5`).
3. Click **Test** — expect an **HTTP 200** response with the AI's answer inside `choices[0].message.content`.
4. Click **Preview Script Usage** and save the generated script for the next step.

## Step 3: Create the Script Include

A **Script Include** is a reusable server-side class you can call from other scripts.

1. Navigate to **All → System Definition → Script Includes** (or `sys_script_include.list`).
2. Click **New**.
   - **Name**: `ChatGPTOpenAI`.
   - **Script**: paste the script from *Preview Script Usage*, then adapt it to call the REST message and parse the chat response. A minimal version:
   ```js
   var ChatGPTOpenAI = Class.create();
   ChatGPTOpenAI.prototype = Object.extendsObject(AbstractAjaxProcessor, {
     askChatGPT: function(prompt) {
       try {
         var rest = new sn_ws.RESTMessageV2('ChatGPT', 'POST');
         rest.setStringParameterNoEscape('prompt', prompt);
         rest.setStringParameterNoEscape('model', 'gpt-4o-mini');
         var response = rest.execute();
         var body = new JSON().decode(response.getBody());
         var answer = body.choices[0].message.content;
         return answer;
       } catch (e) {
         return 'Sorry, I could not reach the AI service.';
       }
     },
     type: 'ChatGPTOpenAI'
   });
   ```
3. Click **Submit**.

## Step 4: Create a Flow Designer Action

Wrap the script call in a reusable **Action** so the Virtual Agent can invoke it.

1. Open **All → Process Automation → Flow Designer**.
2. Click **New → Action**, name it `askChatGPTOpenAi`, and save.
3. Click **Inputs** and add an action input:
   - **Name**: `prompt`, **Type**: String, **Mandatory**: true.
4. Click the **+** after Inputs, search for **Script**, and add the Script step.
5. For the script step:
   - **Create variable** for its input, e.g. `scriptPrompt`, and map it to the action's `prompt`.
   - In the script section, call the Script Include:
     ```js
     (function execute(inputs, outputs) {
       var bot = new ChatGPTOpenAI();
       outputs.answer = bot.askChatGPT(inputs.scriptPrompt);
     })(inputs, outputs);
     ```
6. Create an **output variable** `answer` (String) for the script step.
7. Under **Action Outline → Outputs**, add an action output variable (e.g. `answer`) and map it to the script's `answer` output.
8. Save and **Activate** the action.

## Step 5: Build the Virtual Agent Topic

1. Navigate to **All → Conversational Interfaces → Virtual Agent → Virtual Agent Designer**.
2. Click **Create → Topic**, name it **Ask ChatGPT**, and save.
3. Build the conversation:
   - **User Question**: *"What would you like to ask?"* → store as `prompt`.
   - **Condition**: if `prompt` is empty → **End Conversation** with a goodbye message; otherwise continue.
   - **Action utility**: select the **askChatGPTOpenAi** action, pass in the user's `prompt`.
   - **Message**: show the action's `answer` output as the bot's reply.
4. Publish the topic (and the assistant it belongs to).

## Step 6: Test End to End

1. Open the **Service Portal** and start a chat with your assistant.
2. Type a question such as *"What is ServiceNow?"*.
3. The topic runs, calls OpenAI, and the bot replies with the AI's answer.

## Troubleshooting

| Problem | Likely cause |
| --- | --- |
| 401 Unauthorized | API key missing/mistyped, or `Bearer ` prefix wrong |
| 404 / 405 | Wrong endpoint or HTTP method (must be POST `/v1/chat/completions`) |
| 400 Bad Request | Body format wrong — ensure `messages` array with `role` + `content` |
| Empty answer | Wrong JSON path — answer lives in `choices[0].message.content` |
| Building it without a key | Point the REST Message at `https://httpbin.org/post` and read `body.json.prompt` — see the callout at the top of this lesson |
| Topic doesn't trigger | Assistant/topic not **published**, or NLU not matched |

## Key Takeaways

- A **REST message** calls OpenAI's **chat completions** endpoint (not the legacy completions endpoint).
- A **Script Include** wraps the call so other scripts can reuse it.
- A **Flow Designer Action** exposes the call to Virtual Agent as a reusable step.
- A **Virtual Agent topic** turns a user's chat input into the AI request and displays the answer.
- Test each layer (REST → script → action → topic) before wiring them together.
