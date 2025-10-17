from observer.handlers.handler import Handler
import message_parser
import tg_handler


class WrongCommandHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        return True

    def handle(self, message: dict) -> bool:
        tg_handler.send_text(
            message_parser.get_id(message), "Sorry, you enter wrong command"
        )
        return False
