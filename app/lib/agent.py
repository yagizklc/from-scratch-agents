from typing import Any, Mapping
from .chat import Chat, Message
from .tool import Tool
from .llm import LLM


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
        tool_name, params = self._parse_output_to_action(output=output)

        tools = {t.__name__.lower(): t for t in self._current_tools}
        if tool_name.lower() not in tools:
            raise Exception("not a valid tool")

        tool = tools[tool_name]
        observation = tool.use(**params)

        new_prompt = prompt + output + observation
        return self._llm.observe(new_prompt)

    @property
    def current_tools(self) -> list[type[Tool]]:
        return self._current_tools

    def _parse_output_to_action(self, output: str) -> tuple[str, Mapping[str, Any]]:
        return ("", {})
