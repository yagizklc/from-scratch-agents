from .lib import Message, Agent
from .config import Tools


def main() -> None:
    # Create DynamicChat instance with no initial tools
    agent = Agent()

    # Main chat loop
    print("Chat started! (Type 'quit' to exit, 'tools' to modify tools)")
    while True:
        user_input = input(">")

        if user_input.lower() in ("q", "quit", "exit"):
            break

        if user_input.lower() == "tools":
            print("\nTools Management:")
            print("1. Add tools")
            print("2. Remove tools")
            print("3. Show current tools")
            print("4. Cancel")

            choice = input("Select option (1-4): ")

            if choice == "1":
                # Show available tools that aren't currently selected
                available = [t for t in Tools if t not in agent.current_tools]
                if not available:
                    print("No additional tools available!")
                    continue

                print(
                    "Available Tools:",
                    [f"{t.__name__} ({i+1})" for i, t in enumerate(available)],
                )

                try:
                    indices = [
                        int(x.strip()) - 1
                        for x in input("Select tools to add: ").split(",")
                    ]
                    new_tools = [
                        available[i] for i in indices if 0 <= i < len(available)
                    ]
                    agent.add_tools(new_tools)
                    print(f"Added tools: {[t.__name__ for t in new_tools]}")
                except (ValueError, IndexError):
                    print("Invalid selection!")

            elif choice == "2":
                # Show current tools for removal
                current = agent.current_tools
                if not current:
                    print("No tools currently active!")
                    continue

                print(
                    "Current Tools:",
                    [f"{t.__name__} ({i+1})" for i, t in enumerate(current)],
                )

                try:
                    indices = [
                        int(x.strip()) - 1
                        for x in input("Select tools to remove: ").split(",")
                    ]
                    to_remove = [current[i] for i in indices if 0 <= i < len(current)]
                    agent.remove_tools(to_remove)
                    print(f"Removed tools: {[t.__name__ for t in to_remove]}")
                except (ValueError, IndexError):
                    print("Invalid selection!")

            elif choice == "3":
                if not agent.current_tools:
                    print("No tools currently active")
                else:
                    print("Current Tools:", [t.__name__ for t in agent.current_tools])

            continue

        agent.submit_message(message=Message(content=user_input))

    print("\nbye")


if __name__ == "__main__":
    main()
