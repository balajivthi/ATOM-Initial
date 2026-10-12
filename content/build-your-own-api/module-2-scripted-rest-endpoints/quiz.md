# Quiz: Scripted REST Endpoints

Answer these questions about building, securing, and testing Scripted REST APIs. Your score is saved, and reasoning is revealed after you submit.

1. In a Scripted REST resource path like `order/{order_number}`, how do you read the order number in the script?
   A. request.body.data.order_number
   B. request.queryParams.order_number
   C. request.pathParams.order_number
   D. request.headers.order_number
   CORRECT: C
   EXPLAIN: Curly-brace segments in the resource path are path parameters, read via `request.pathParams.order_number`.

2. Which line correctly sends the response body from a Scripted REST method?
   A. return "body";
   B. response.setBody(JSON.stringify(data))
   C. response.write(data)
   D. response.body = data
   CORRECT: B
   EXPLAIN: `response.setBody()` takes a string (typically a `JSON.stringify` result); `response.setStatus()` sets the HTTP code.

3. A caller without the required role receives which HTTP status?
   A. 200
   B. 401
   C. 403
   D. 404
   CORRECT: C
   EXPLAIN: `401` means not authenticated; `403` means authenticated but not authorized (missing the required role).

4. What is the correct status code for successfully creating a resource via POST?
   A. 200
   B. 201
   C. 301
   D. 400
   CORRECT: B
   EXPLAIN: `201 Created` is the convention for a successful POST; `200` is used for reads/updates that don't create.

5. Which object do you read to get the JSON sent in the request body?
   A. request.pathParams
   B. request.queryParams
   C. request.body.data
   D. request.session
   CORRECT: C
   EXPLAIN: The parsed JSON request body is available as `request.body.data` for POST/PUT/PATCH methods.

6. Why should a Scripted REST API validate its input and return JSON errors?
   A. To make the API slower and harder to use
   B. Because external callers are untrusted and need clear, consistent failures
   C. To hide the API from search engines
   D. Because HTML responses are forbidden by HTTP
   CORRECT: B
   EXPLAIN: External integrations will send bad data; validating input and returning consistent JSON + correct status codes (400/404/500) makes failures predictable and safe.
