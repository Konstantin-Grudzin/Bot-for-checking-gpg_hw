import message_parser
import tg_handler
from observer.handlers.handler import Handler

supported_fields = {
    "message": ["text", "document"],
}


class UnsupportedTypesHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        msg_type = message_parser.get_msg_type(message)
        return not any(
            field in message[msg_type] for field in supported_fields.get(msg_type, [])
        )

    def handle(self, message: dict) -> bool:
        tg_handler.send_text(
            message_parser.get_id(message), "Sorry, I can't handle this message"
        )
        return False
