# Quiz: Virtual Agent & AI Integration

Answer these questions about Virtual Agent and the ChatGPT integration. Your score is saved, and reasoning is revealed after you submit.

1. What is a single conversation the Virtual Agent can hold called?
   A. A topic
   B. A script
   C. A catalog item
   D. A widget
   CORRECT: A
   EXPLAIN: Topics are individual conversations (e.g. "Ask ChatGPT", "Reset Password") authored in the Virtual Agent Designer.

2. Where are Virtual Agent topics built?
   A. System Definition → Script Includes
   B. Conversational Interfaces → Virtual Agent Designer
   C. Service Catalog → Maintain Items
   D. System Web Services → REST Message
   CORRECT: B
   EXPLAIN: The Virtual Agent Designer (under Conversational Interfaces) is the visual canvas for authoring topics.

3. Which is the CURRENT OpenAI endpoint for chat?
   A. POST /v1/completions
   B. POST /v1/chat/completions
   C. GET /v1/models
   D. POST /v1/embeddings
   CORRECT: B
   EXPLAIN: Use `https://api.openai.com/v1/chat/completions`. The old `/v1/completions` endpoint is legacy and not supported by current models.

4. In the chat-completions body, where does the user's question go?
   A. In a "prompt" string only
   B. In a "messages" array with "role" and "content"
   C. In the Authorization header
   D. In the endpoint URL
   CORRECT: B
   EXPLAIN: The body sends a `messages` array (e.g. `{"role":"user","content":"..."}`) along with the model name.

5. What wraps the REST call so it can be reused from other server scripts?
   A. A client script
   B. A Script Include
   C. A virtual agent topic
   D. A UI policy
   CORRECT: B
   EXPLAIN: A Script Include (e.g. ChatGPTOpenAI) is a reusable server-side class; a Flow Designer Action then exposes it to Virtual Agent.
