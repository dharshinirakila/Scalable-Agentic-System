from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Tool:
    name: str
    description: str
    category: str
    parameters: list[str]
    function: Callable[..., Any]

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def search(self, query: str, limit: int = 5) -> list[Tool]:
        # Demo keyword search. Production can use hybrid/vector search.
        words = set(query.lower().replace("?", "").replace(",", "").split())
        scored = []
        for tool in self.tools.values():
            text = (
                f"{tool.name} {tool.description} {tool.category} "
                f"{' '.join(tool.parameters)}"
            ).lower()
            score = sum(1 for word in words if word in text)
            if score:
                scored.append((score, tool))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [tool for _, tool in scored[:limit]]

    def get(self, name: str):
        return self.tools.get(name)

    def all_tools(self):
        return list(self.tools.values())
