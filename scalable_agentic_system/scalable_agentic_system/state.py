from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    user_request: str
    intent: str = ""
    selected_tool: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    tool_result: Any = None
    errors: list[str] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add_history(self, step: str, data: Any) -> None:
        self.history.append({"step": step, "data": data})
