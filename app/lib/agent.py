from .chat import Chat, Message
from .tool import Tool


class Agent:
    """A wrapper class that handles dynamic Tool management for Chat instances"""

    def __init__(self, tools: list[type[Tool]] = []) -> None:
        self._chat = Chat(tools=tools)
        self._current_tools = tools or []

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

    def submit_message(self, message: Message) -> None:
        self._chat.submit_message(message=message)

    @property
    def current_tools(self) -> list[type[Tool]]:
        return self._current_tools
