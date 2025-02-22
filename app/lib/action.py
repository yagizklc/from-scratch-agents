from typing import Any
from pydantic import BaseModel


class Action(BaseModel):
    tool_name: str
    params: dict[str, Any]
