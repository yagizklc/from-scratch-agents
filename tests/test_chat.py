import pytest
from pydantic import ValidationError

from app.lib.chat import Message, Chat


def test_message_creation():
    # Test default role
    message = Message(content="Hello")
    assert message.role == "user"
    assert message.content == "Hello"

    # Test custom role
    message = Message(role="assitant", content="Hi there")
    assert message.role == "assitant"
    assert message.content == "Hi there"

    # Test invalid role
    with pytest.raises(ValidationError):
        Message(role="invalid_role", content="test")  # type:ignore


def test_chat_creation():
    chat = Chat(
        system_message="You are a helpful assistant",
        previous_messages=[],
        _chat_history="",
    )
    assert chat.system_message == "You are a helpful assistant"
    assert chat.previous_messages == []


def test_chat_history_empty():
    chat = Chat(
        system_message="You are a helpful assistant",
        previous_messages=[],
        _chat_history="",
    )
    expected = """
        <|im_start|>system
        You are a helpful assistant
        <|im_end|>
        """
    assert chat.chat_history.strip() == expected.strip()


def test_chat_history_with_messages():
    messages = [
        Message(role="user", content="Hello"),
        Message(role="assitant", content="Hi there"),
        Message(role="user", content="How are you?"),
    ]

    chat = Chat(
        system_message="You are a helpful assistant",
        previous_messages=messages,
        _chat_history="",
    )

    expected = """
        <|im_start|>system
        You are a helpful assistant
        <|im_end|>

        <|im_start|>user
        How are you?<|im_end|>

        <|im_start|>assitant
        Hi there<|im_end|>

        <|im_start|>user
        Hello<|im_end|>
        """

    assert chat.chat_history.strip() == expected.strip()


def test_submit_message():
    chat = Chat(
        system_message="You are a helpful assistant",
        previous_messages=[],
        _chat_history="",
    )

    new_message = Message(role="user", content="Hello")
    result = chat.submit_message(new_message)

    expected = """
        <|im_start|>system
        You are a helpful assistant
        <|im_end|>

        <|im_start|>user
        Hello<|im_end|>
        """

    assert result.strip() == expected.strip()


def test_empty_content():
    # Test empty content in message
    with pytest.raises(ValidationError):
        Message(content="")


def test_whitespace_handling():
    chat = Chat(
        system_message="System",
        previous_messages=[Message(content="  Message with spaces  ")],
        _chat_history="",
    )

    # Check that whitespace is preserved in the chat history
    assert "  Message with spaces  " in chat.chat_history


def test_multiple_messages_order():
    messages = [
        Message(content="First"),
        Message(content="Second"),
        Message(content="Third"),
    ]

    chat = Chat(system_message="System", previous_messages=messages, _chat_history="")

    # Messages should appear in reverse order in chat history
    history = chat.chat_history
    first_pos = history.find("First")
    second_pos = history.find("Second")
    third_pos = history.find("Third")

    assert first_pos > second_pos > third_pos


def test_special_characters():
    special_msg = Message(content="Special chars: !@#$%^&*()\n\t")
    chat = Chat(
        system_message="System", previous_messages=[special_msg], _chat_history=""
    )

    assert "Special chars: !@#$%^&*()\n\t" in chat.chat_history
