import GPGHandler
import JsonHelper
import TgHandler
from UserMaster.UserHelper import (
    userState,
    menuText,
    menuButtons,
    tgCommand,
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
from secret_info.CanPass import canPass


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.state = userState(data["state"])
        self.username = data["username"]
        self.result = data["result"]

    def changeState(self, state):
        print(state)
        self.state = state
        JsonHelper.changeState(self.id, state)
        TgHandler.sendText(self.id, menuText[state], menuButtons[state])

    def stateHandler(self, message):
        match self.state:
            case userState.BEGIN:
                return self.BeginHandler(message)
            case userState.CHANGE_NAME:
                return self.ChangeNameHandler(message)
            case userState.ENTER_ADMIN:
                return self.EnterAdminHandler(message)
            case userState.ADMIN:
                return self.AdminHandler(message)
            case userState.WAIT_FOR_GPG:
                return self.WaitForGPGHandler(message)
            case userState.WAIT_FOR_CORRECT_MESSAGE:
                return self.WaitForCorrectMessage(message)
            case _:
                return self.BeginHandler(message)

    # ======================================HANDLERS======================================
    def BeginHandler(self, message):
        match message:
            case tgCommand.START.value:
                TgHandler.sendText(self.id, gen_start_text(self))
                return userState.BEGIN
            case tgCommand.CHANGE_NAME.value:
                return userState.CHANGE_NAME
            case tgCommand.BECOME_ADMIN.value:
                return self.EnterAdminHandler(self.id)
            case tgCommand.BEGIN_EXAM.value:
                return userState.WAIT_FOR_GPG
            case _:
                TgHandler.sendText(self.id, wrong_command)
                return userState.BEGIN

    def ChangeNameHandler(self, message):
        match message:
            case tgCommand.EXIT.value:
                pass
            case _:
                self.username = message
                try:
                    JsonHelper.changeName(self.id, message)
                except Exception:
                    TgHandler.sendText(self.id, "Sorry Something Went Wrong")
                    return userState.BEGIN
                TgHandler.sendText(self.id, success_name_changing(self))
        return userState.BEGIN

    def EnterAdminHandler(self, id):
        if canPass(id):
            AdminPanel.AddAdmin(self.id)
            TgHandler.sendText(self.id, "Приветствую, Милорд")
            return userState.ADMIN
        else:
            TgHandler.sendText(self.id, wrong_admin_data)
            return userState.BEGIN

    def AdminHandler(self, message):
        match message:
            case tgCommand.EXIT.value:
                AdminPanel.DelAdmin(self.id)
                return userState.BEGIN
            case tgCommand.ADMIN_NOTIFY_ON.value:
                TgHandler.sendText(self.id, admin_notify_on)
                AdminPanel.OnNotify(self.id)
                return userState.ADMIN
            case tgCommand.ADMIN_NOTIFY_OFF.value:
                TgHandler.sendText(self.id, admin_notify_off)
                AdminPanel.OffNotify(self.id)
                return userState.ADMIN
            case _:
                TgHandler.sendText(self.id, wrong_command)
                return userState.ADMIN

    def WaitForGPGHandler(self, message):
        match message:
            case tgCommand.EXIT.value:
                TgHandler.sendText(self.id, your_gpg_key_delete)
                GPGHandler.deleteGPG(self.id)
                return userState.BEGIN
            case _:
                if GPGHandler.addGPG(self.id, message):
                    TgHandler.sendText(self.id, your_gpg_added)
                    TgHandler.sendGPGMessage(self.id, GPGHandler.getMessage(self.id))
                    return userState.WAIT_FOR_CORRECT_MESSAGE
                TgHandler.sendText(self.id, incorrect_gpg)
                return userState.WAIT_FOR_GPG

    def WaitForCorrectMessage(self, message):
        match message:
            case tgCommand.EXIT.value:
                TgHandler.sendText(self.id, your_gpg_key_delete)
                GPGHandler.deleteGPG(self.id)
                return userState.BEGIN
            case _:
                if GPGHandler.getDecMessage(self.id) == message:
                    TgHandler.sendText(self.id, you_are_correct)
                    if not self.result:
                        AdminPanel.AddGoodStudent(self.username)
                        self.result = True
                        JsonHelper.changeResult(self.id)
                    GPGHandler.deleteGPG(self.id)
                    return userState.BEGIN
                TgHandler.sendText(self.id, incorrect_message)
                return userState.WAIT_FOR_CORRECT_MESSAGE
