# Architecture Explanation

## Goal
Handle natural-language requests against hundreds or thousands of APIs without exposing every tool to the model at every step.

## Flow
User -> Agent -> Intent Detection -> Tool Search -> Tool Selection -> RAG Context -> Parameter Validation -> Tool Execution -> State -> Response

## Scaling
1. Store tool metadata in a registry.
2. Search the registry and return only a small candidate set.
3. Select the best tool from those candidates.
4. Validate its input schema.
5. Execute the tool.
6. Store results in state.
7. Add retries/timeouts/circuit breakers around real APIs.

## Production improvements
- Replace mock PayPal functions with authenticated API clients.
- Use OAuth and a secret manager.
- Use vector/hybrid search for a large tool catalog.
- Add authorization and approval for sensitive operations.
- Add rate limits, audit logs, metrics and tracing.
- Add unit/integration tests.
- Use LangGraph or another workflow framework if the production workflow becomes more complex.
