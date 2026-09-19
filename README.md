# Scalable Agentic System

A runnable Python prototype for the scalable agentic-system assignment.

It demonstrates:
- Tool registry and tool search/routing
- PayPal-style invoice, sales, and dispute tools
- RAG-style documentation search
- System search
- Parameter validation
- State management
- Error handling
- Scaling from a few tools toward hundreds/thousands

## Run
Python 3.10+ is recommended.

```bash
python main.py
```

No API key is required because PayPal calls are mocked for the demo.

## Structure

- `main.py` - runs the examples
- `agent.py` - agent workflow
- `tool_registry.py` - scalable tool registry/search
- `tools.py` - mock API tools and validation
- `rag.py` - local RAG-style documentation search
- `state.py` - agent state
- `ARCHITECTURE.md` - design explanation
- `requirements.txt` - dependencies

## Important
This is a local prototype, not a real payment system. Replace mock functions with authenticated APIs for production.
