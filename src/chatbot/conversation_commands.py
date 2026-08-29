EXIT_COMMANDS = {
    "exit",
    "quit",
    "bye",
    "goodbye",
    "stop",
    "cancel",
    "end",
    "bas ho gaya",
    "band karo",
    "conversation end",
    "close"
}


def is_exit_command(message: str) -> bool:

    message = message.lower().strip()

    return message in EXIT_COMMANDS