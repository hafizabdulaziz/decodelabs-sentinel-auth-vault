import abc
from typing import Any


class BaseAgentTool(abc.ABC):
    @abc.abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        pass

class BaseSecurityAgent(abc.ABC):
    def __init__(self, name: str):
        self.name = name
        self.tools: list[BaseAgentTool] = []

    def add_tool(self, tool: BaseAgentTool):
        self.tools.append(tool)

    @abc.abstractmethod
    async def run_command(self, command: str) -> str:
        pass
