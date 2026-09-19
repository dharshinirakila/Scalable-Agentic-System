from agent import Agent

def print_case(agent: Agent, request: str):
    print("=" * 72)
    print("USER:", request)
    state = agent.run(request)
    print("SELECTED TOOL:", state.selected_tool)
    print("PARAMETERS:", state.parameters)
    print("RESPONSE:", agent.format_response(state))
    if state.errors:
        print("ERRORS:", state.errors)
    print("STATE STEPS:")
    for item in state.history:
        print(f"  - {item['step']}: {item['data']}")

def main():
    agent = Agent()

    print_case(agent, "Send an invoice for $50")
    print_case(agent, "What was my total sales volume last month?")
    print_case(agent, "Is there a dispute open from user_123?")

    print("=" * 72)
    print("SYSTEM SEARCH: invoice")
    for tool in agent.system_search("invoice"):
        print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    main()

