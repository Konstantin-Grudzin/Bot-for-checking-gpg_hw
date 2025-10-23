import gpg_handler
import message_parser
import tg_handler
from observer.handlers.handler import Handler
from secret_info.can_pass import can_pass
from user import User
from user_helper import (
    TgCommand,
    UserState,
    check_you_info,
    your_gpg_key_delete,
    your_gpg_added,
    incorrect_gpg,
    wrong_command,
    you_are_correct,
    incorrect_message,
)


class StartHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        return message_parser.get_text(message) == "/start"

    def handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        if can_pass(user.id):
            user.change_state(UserState.ADMIN)
        else:
            user.change_state(UserState.BEGIN)
        return False


class EnterExamHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        return (
            user.state == UserState.BEGIN
            and message_parser.get_text(message) == TgCommand.BEGIN_EXAM.value
        )

    def handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        if user.result:
            tg_handler.send_text(user.id, "You already pass the exam")
        else:
            user.change_state(UserState.WAIT_FOR_GPG)
        return False


class AdminHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        return user.state == UserState.ADMIN

    def handle(self, message: dict) -> bool:
        match message_parser.get_text(message):
            case TgCommand.PRINT_ALL_PASSED.value:
                tg_handler.print_all_passed()
            case TgCommand.EXIT.value:
                user = User(message_parser.get_id(message))
                user.change_state(UserState.BEGIN)
            case _:
                return True

        return False


class WaitForGPGHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        return user.state == UserState.WAIT_FOR_GPG

    def handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        if message_parser.get_text(message) == TgCommand.EXIT.value:
            tg_handler.send_text(user.id, your_gpg_key_delete)
            gpg_handler.delete_gpg(user.id)
            user.change_state(UserState.BEGIN)
        else:
            text = message_parser.get_text_or_file(message)
            error = gpg_handler.add_gpg(user.id, text)
            if error is None:
                tg_handler.send_text(user.id, your_gpg_added)
                user.set_exam_info(gpg_handler.get_info_from_key(user.id))
                tg_handler.send_text(user.id, check_you_info(user))
                user.change_state(UserState.USER_CHECK_GPG)
            else:
                tg_handler.send_text(user.id, incorrect_gpg)
                tg_handler.send_text(user.id, error)
                user.change_state(UserState.WAIT_FOR_GPG)
        return False


class CheckGPGHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        return user.state == UserState.USER_CHECK_GPG

    def handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        match message_parser.get_text(message):
            case TgCommand.EXIT.value:
                tg_handler.send_text(user.id, your_gpg_key_delete)
                gpg_handler.delete_gpg(user.id)
                user.change_state(UserState.BEGIN)
            case TgCommand.OK.value:
                tg_handler.send_big_text(user.id, gpg_handler.get_message(user.id))
                user.change_state(UserState.WAIT_FOR_CORRECT_MESSAGE)
            case TgCommand.NO.value:
                user.change_state(UserState.WAIT_FOR_GPG)
                gpg_handler.delete_gpg(user.id)
            case _:
                tg_handler.send_text(user.id, wrong_command)
        return False


class WaitForCorrectMessageHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        return user.state == UserState.WAIT_FOR_CORRECT_MESSAGE

    def handle(self, message: dict) -> bool:
        user: User = User(message_parser.get_id(message))
        match message_parser.get_text(message):
            case TgCommand.EXIT.value:
                tg_handler.send_text(user.id, your_gpg_key_delete)
                gpg_handler.delete_gpg(user.id)
                user.change_state(UserState.BEGIN)
            case _:
                if gpg_handler.get_dec_message(
                    user.id
                ) == message_parser.get_text_or_file(message):
                    tg_handler.send_text(user.id, you_are_correct)
                    if not user.result:
                        user.change_result()
                    gpg_handler.delete_gpg(user.id)
                    user.change_state(UserState.BEGIN)
                    return False
                tg_handler.send_text(user.id, incorrect_message)
                user.change_state(UserState.WAIT_FOR_CORRECT_MESSAGE)
        return False
