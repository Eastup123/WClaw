from pathlib import Path
from typing import Any

from agent import create_agent
from runtime.formatting import extract_stream_text, format_agent_result
from utils import load_settings


EXIT_COMMANDS = {"exit", "quit", "q", ":q"}


def _stream_agent_reply(agent: Any, messages: list[Any]) -> dict[str, Any] | None:
    last_values: dict[str, Any] | None = None
    active_message_id: str | None = None
    printed_by_message_id: dict[str, str] = {}
    started_reply = False

    for mode, payload in agent.stream(
        {"messages": messages},
        stream_mode=["messages", "values"],
    ):
        if mode == "messages":
            message, metadata = payload
            if metadata.get("langgraph_node") != "model":
                continue

            text = extract_stream_text(message)
            if not text:
                continue

            message_id = getattr(message, "id", None) or f"msg-{len(printed_by_message_id)}"
            already_printed = printed_by_message_id.get(message_id, "")
            if text.startswith(already_printed):
                delta = text[len(already_printed) :]
            else:
                delta = text
            if not delta:
                continue

            if message_id != active_message_id:
                if started_reply:
                    print()
                print("WClaw> ", end="", flush=True)
                active_message_id = message_id
                started_reply = True

            print(delta, end="", flush=True)
            printed_by_message_id[message_id] = already_printed + delta
        elif mode == "values":
            last_values = payload

    if started_reply:
        print()

    return last_values


def run_demo(config_path: str | Path = "config/config.yaml") -> None:
    settings = load_settings(config_path)
    agent = create_agent(settings)
    messages: list[Any] = []

    print("Interactive chat started. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou> ").strip()
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Session ended.")
            break

        messages.append({"role": "user", "content": user_input})
        result = _stream_agent_reply(agent, messages)
        if isinstance(result, dict):
            state_messages = result.get("messages")
            if isinstance(state_messages, list):
                messages = state_messages
            else:
                assistant_text = format_agent_result(result)
                if assistant_text:
                    messages.append({"role": "assistant", "content": assistant_text})
