import GPGHandler
import JsonHelper
import TgHandler
from UserMaster.UserHelper import (
    UserState,
    menu_text,
    menu_buttons,
    TgCommand,
    gen_start_text,
    success_name_changing,
    wrong_command,
    wrong_admin_data,
    your_gpg_key_delete,
    your_gpg_added,
    incorrect_gpg,
    you_are_correct,
    incorrect_message,
    admin_notify_on,
    admin_notify_off,
)
import AdminPanel
from secret_info.CanPass import can_pass


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.state = UserState(data["state"])
        self.username = data["username"]
        self.result = data["result"]

    def change_state(self, state):
        print(state)
        self.state = state
        JsonHelper.change_state(self.id, state)
        TgHandler.send_text(self.id, menu_text[state], menu_buttons[state])

    def state_handler(self, message):
        match self.state:
            case UserState.BEGIN:
                return self.begin_handler(message)
            case UserState.CHANGE_NAME:
                return self.change_name_handler(message)
            case UserState.ENTER_ADMIN:
                return self.enter_admin_handler(message)
            case UserState.ADMIN:
                return self.admin_handler(message)
            case UserState.WAIT_FOR_GPG:
                return self.wait_for_gpg_handler(message)
            case UserState.WAIT_FOR_CORRECT_MESSAGE:
                return self.wait_for_correct_message(message)
            case _:
                return self.begin_handler(message)

    # ======================================HANDLERS======================================
    def begin_handler(self, message):
        match message:
            case TgCommand.START.value:
                TgHandler.send_text(self.id, gen_start_text(self))
                return UserState.BEGIN
            case TgCommand.CHANGE_NAME.value:
                return UserState.CHANGE_NAME
            case TgCommand.BECOME_ADMIN.value:
                return self.enter_admin_handler(self.id)
            case TgCommand.BEGIN_EXAM.value:
                return UserState.WAIT_FOR_GPG
            case _:
                TgHandler.send_text(self.id, wrong_command)
                return UserState.BEGIN

    def change_name_handler(self, message):
        match message:
            case TgCommand.EXIT.value:
                pass
            case _:
                self.username = message
                try:
                    JsonHelper.change_name(self.id, message)
                except Exception:
                    TgHandler.send_text(self.id, "Sorry Something Went Wrong")
                    return UserState.BEGIN
                TgHandler.send_text(self.id, success_name_changing(self))
        return UserState.BEGIN

    def enter_admin_handler(self, id):
        if can_pass(id):
            AdminPanel.add_admin(self.id)
            TgHandler.send_text(self.id, "Приветствую, Милорд")
            return UserState.ADMIN
        else:
            TgHandler.send_text(self.id, wrong_admin_data)
            return UserState.BEGIN

    def admin_handler(self, message):
        match message:
            case TgCommand.EXIT.value:
                AdminPanel.del_admin(self.id)
                return UserState.BEGIN
            case TgCommand.ADMIN_NOTIFY_ON.value:
                TgHandler.send_text(self.id, admin_notify_on)
                AdminPanel.on_notify(self.id)
                return UserState.ADMIN
            case TgCommand.ADMIN_NOTIFY_OFF.value:
                TgHandler.send_text(self.id, admin_notify_off)
                AdminPanel.off_notify(self.id)
                return UserState.ADMIN
            case _:
                TgHandler.send_text(self.id, wrong_command)
                return UserState.ADMIN

    def wait_for_gpg_handler(self, message):
        match message:
            case TgCommand.EXIT.value:
                TgHandler.send_text(self.id, your_gpg_key_delete)
                GPGHandler.delete_gpg(self.id)
                return UserState.BEGIN
            case _:
                if GPGHandler.add_gpg(self.id, message):
                    TgHandler.send_text(self.id, your_gpg_added)
                    TgHandler.send_gpg_message(self.id, GPGHandler.get_message(self.id))
                    return UserState.WAIT_FOR_CORRECT_MESSAGE
                TgHandler.send_text(self.id, incorrect_gpg)
                return UserState.WAIT_FOR_GPG

    def wait_for_correct_message(self, message):
        match message:
            case TgCommand.EXIT.value:
                TgHandler.send_text(self.id, your_gpg_key_delete)
                GPGHandler.delete_gpg(self.id)
                return UserState.BEGIN
            case _:
                if GPGHandler.get_dec_message(self.id) == message:
                    TgHandler.send_text(self.id, you_are_correct)
                    if not self.result:
                        AdminPanel.add_good_student(self.username)
                        self.result = True
                        JsonHelper.change_result(self.id)
                    GPGHandler.delete_gpg(self.id)
                    return UserState.BEGIN
                TgHandler.send_text(self.id, incorrect_message)
                return UserState.WAIT_FOR_CORRECT_MESSAGE
