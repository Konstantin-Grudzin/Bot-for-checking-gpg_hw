import tg_handler


def get_file_id(x):
    return x.get("document", {}).get("file_id", None)


def get_id(message: dict) -> int:
    type = get_msg_type(message)
    return message[type]["chat"]["id"]


def get_text(message: dict) -> str | None:
    type = get_msg_type(message)
    return message[type].get("text", None)


def get_msg_type(message: dict) -> str:
    return [*message.keys()][1]


def get_text_or_file(message: dict) -> str | None:
    type = get_msg_type(message)
    text = message[type].get("text", None)
    if text is None and get_file_id(message[type]) is not None:
        text = tg_handler.get_file(get_file_id(message[type]))
    return text
