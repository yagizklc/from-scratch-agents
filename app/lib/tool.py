from abc import abstractmethod
from typing import Any
from pydantic import BaseModel


class Tool(BaseModel):
    @classmethod
    def tool_schema(cls) -> str:
        """Format a single tool's information for the system message."""
        return f"Tool Schema: {cls.model_json_schema()}"

    # NOTE: implement this for your tool
    @abstractmethod
    def use(self, *args, **kwargs) -> str: ...


class Action(BaseModel):
    tool_name: str
    params: list[tuple[str, Any]]
