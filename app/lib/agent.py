from typing import Any, Mapping

import json
import re

from .chat import Chat, Message
from .llm import LLM
from .tool import Tool
from .action import Action


class Agent:
    """A wrapper class that handles dynamic Tool management for Chat instances"""

    def __init__(
        self,
        llm: LLM,
        tools: list[type[Tool]] = [],
    ) -> None:
        self._chat = Chat(tools=tools)
        self._current_tools = tools or []
        self._llm = llm

    @property
    def current_tools(self) -> list[type[Tool]]:
        return self._current_tools

    def add_tools(self, new_tools: list[type[Tool]]) -> None:
        updated_tools = list(set(self._current_tools + new_tools))
        new_chat = Chat(_messages=self._chat._messages, tools=updated_tools)
        self._chat = new_chat
        self._current_tools = updated_tools

    def remove_tools(self, tools_to_remove: list[type[Tool]]) -> None:
        updated_tools = [t for t in self._current_tools if t not in tools_to_remove]
        new_chat = Chat(_messages=self._chat._messages, tools=updated_tools)
        self._chat = new_chat
        self._current_tools = updated_tools

    def submit_message(self, message: Message) -> str:
        self._chat.submit_message(message=message)
        prompt = self._chat._conversation

        output = self._llm.think(prompt=prompt)
        action = self._parse_output_to_action(output=output)

        tools = {t.__name__.lower(): t for t in self._current_tools}
        if action.action.lower() not in tools:
            raise Exception("not a valid tool")

        observation = tools[action.action].use(**action.action_input)
        new_prompt = prompt + output + observation
        return self._llm.observe(new_prompt)

    def _parse_output_to_action(self, output: str) -> Action:
        # Find JSON block between triple backticks
        json_match = re.search(r"```(?:json\n)?({[^}]+})```", output)
        if not json_match:
            raise ValueError("No valid JSON action block found in output")

        action_block = json_match.group(1)
        try:
            return Action.model_validate_json(action_block)
        except Exception as e:
            raise ValueError(f"Failed to parse action JSON: {e}")
