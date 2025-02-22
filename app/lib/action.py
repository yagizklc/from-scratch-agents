from typing import Any
from pydantic import BaseModel


class Action(BaseModel):
    action: str
    action_input: dict[str, Any]
