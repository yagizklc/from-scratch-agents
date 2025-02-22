from typing import Literal, Optional, Self
from pydantic import BaseModel, model_validator
from .tool import Tool
from .config import SYSTEM_MESSAGE

Role = Literal["user", "assitant"]


class Message(BaseModel):
    role: Role = "user"
    content: str


class Chat(BaseModel):
    tools: list[type[Tool]] = []
    _messages: list[Message] = []
    _system_message: Optional[str] = None

    def submit_message(self, message: Message) -> None:
        self._messages.append(message)

    @property
    def _conversation(self) -> str:
        chat_history = f"""
        <|im_start|>system
        {self._system_message}
        <|im_end|>
        """
        for message in reversed(self._messages):
            chat_history = self.__append_message_to_chat_history(
                chat_history=chat_history, message=message
            )

        return chat_history

    def __append_message_to_chat_history(self, chat_history: str, message: Message):
        return f"""
        {chat_history}

        <|im_start|>{ message.role }
        { message.content }<|im_end|>
        """

    @model_validator(mode="after")
    def constuct_system_message(self) -> Self:
        if not self._system_message:
            tool_schemas = "\n        ".join(
                [tool.tool_schema() for tool in self.tools]
            )
            SYSTEM_MESSAGE.format(tool_schemas=tool_schemas)

        return self
