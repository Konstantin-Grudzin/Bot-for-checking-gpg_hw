from observer.handlers.sql_handler import SqlHandler
from observer.handlers.unsupported_types_handler import UnsupportedTypesHandler
from observer.handlers.user_state_handlers import (
    StartHandler,
    EnterExamHandler,
    AdminHandler,
    WaitForGPGHandler,
    CheckGPGHandler,
    WaitForCorrectMessageHandler,
)
from observer.handlers.wrong_command_handler import WrongCommandHandler
from observer.handlers.handler import Handler
from user_helper import menu_text, menu_buttons
from user import User
import tg_handler
import message_parser


class Dispatcher:
    handlers: list[Handler] = [
        UnsupportedTypesHandler(),
        SqlHandler(),
        StartHandler(),
        EnterExamHandler(),
        WaitForGPGHandler(),
        CheckGPGHandler(),
        WaitForCorrectMessageHandler(),
        AdminHandler(),
        WrongCommandHandler(),
    ]

    def __call__(self, message: dict):
        for handler in self.handlers:
            if handler.can_handle(message):
                print(handler)
                continue_ = handler.handle(message)
                if not continue_:
                    break
        state = User(message_parser.get_id(message)).state
        print(type(menu_text.get(state, None)), type(menu_buttons.get(state, None)))
        tg_handler.send_text(
            message_parser.get_id(message),
            menu_text.get(state, None),
            menu_buttons.get(state, None),
        )
