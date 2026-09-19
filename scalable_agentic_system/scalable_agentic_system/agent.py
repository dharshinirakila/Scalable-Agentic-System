import re
from datetime import date, timedelta

from rag import RAGTool
from state import AgentState
from tools import TOOL_FUNCTIONS, validate_parameters
from tool_registry import Tool, ToolRegistry

class Agent:
    def __init__(self):
        self.registry = ToolRegistry()
        self.rag = RAGTool()
        self._register_tools()

    def _register_tools(self):
        self.registry.register(Tool(
            "create_invoice",
            "Create and send an invoice for a payment amount",
            "payments invoice billing",
            ["amount", "currency"],
            TOOL_FUNCTIONS["create_invoice"],
        ))
        self.registry.register(Tool(
            "get_sales_volume",
            "Get total sales volume for a date range",
            "reports sales analytics",
            ["start_date", "end_date"],
            TOOL_FUNCTIONS["get_sales_volume"],
        ))
        self.registry.register(Tool(
            "get_dispute",
            "Check whether a user has an open payment dispute",
            "disputes risk users",
            ["user_id"],
            TOOL_FUNCTIONS["get_dispute"],
        ))

    def system_search(self, query: str):
        return self.registry.search(query)

    def detect_intent(self, request: str) -> str:
        text = request.lower()
        if "invoice" in text:
            return "invoice"
        if "sales" in text or "sales volume" in text:
            return "sales"
        if "dispute" in text:
            return "dispute"
        return "unknown"

    def choose_tool(self, intent: str):
        mapping = {
            "invoice": "create_invoice",
            "sales": "get_sales_volume",
            "dispute": "get_dispute",
        }
        return self.registry.get(mapping.get(intent, ""))

    def extract_parameters(self, state: AgentState) -> dict:
        text = state.user_request.lower()
        params = {}

        if state.intent == "invoice":
            match = re.search(r"\$?\s*(\d+(?:\.\d+)?)", text)
            if not match:
                raise ValueError("Could not find invoice amount")
            params["amount"] = float(match.group(1))
            params["currency"] = "USD"

        elif state.intent == "sales":
            today = date.today()
            first_this_month = today.replace(day=1)
            last_previous = first_this_month - timedelta(days=1)
            first_previous = last_previous.replace(day=1)
            params["start_date"] = first_previous.isoformat()
            params["end_date"] = last_previous.isoformat()

        elif state.intent == "dispute":
            match = re.search(r"(user_[a-zA-Z0-9_-]+)", state.user_request)
            if not match:
                raise ValueError("Could not find user_id")
            params["user_id"] = match.group(1)

        return params

    def run(self, request: str) -> AgentState:
        state = AgentState(request)
        try:
            state.intent = self.detect_intent(request)
            state.add_history("intent_detection", state.intent)

            if state.intent == "unknown":
                raise ValueError("Unsupported request")

            candidates = self.system_search(state.intent)
            state.add_history("tool_search", [x.name for x in candidates])

            tool = self.choose_tool(state.intent)
            if not tool:
                raise ValueError("No suitable tool found")

            state.selected_tool = tool.name
            state.add_history("tool_selection", tool.name)

            docs = self.rag.search(tool.description)
            state.add_history("rag_context", docs)

            state.parameters = self.extract_parameters(state)
            validate_parameters(tool.name, state.parameters)
            state.add_history("parameter_validation", state.parameters)

            state.tool_result = tool.function(**state.parameters)
            state.add_history("tool_execution", state.tool_result)

        except Exception as exc:
            state.errors.append(str(exc))
            state.add_history("error", str(exc))

        return state

    def format_response(self, state: AgentState) -> str:
        if state.errors:
            return "Error: " + state.errors[-1]

        result = state.tool_result
        if state.intent == "invoice":
            return (
                f"Invoice created successfully. ID={result['invoice_id']}, "
                f"Amount={result['currency']} {result['amount']:.2f}"
            )
        if state.intent == "sales":
            return (
                f"Sales volume from {result['start_date']} to {result['end_date']}: "
                f"{result['currency']} {result['total_sales_volume']:.2f}"
            )
        if state.intent == "dispute":
            if result["open_dispute"]:
                return (
                    f"An open dispute exists for {result['user_id']}. "
                    f"Dispute ID={result['dispute_id']}"
                )
            return f"No open dispute was found for {result['user_id']}."
        return str(result)
