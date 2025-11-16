# App Imports
from utils.json import dumpify


def format_message(message):
    assert message is not None, "Message shouldn't be None"
    return f"data: {dumpify(message)}\n\n"
