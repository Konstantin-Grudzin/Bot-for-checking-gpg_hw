import json

import requests
import JsonHelper
from UserMaster.User import User
from secret_info import address
from UserMaster.UserHelper import userState, tgCommand


def sendMessage(user_inst: User):
    requests.post(
        address + "sendMessage",
        params={
            "chat_id": user_inst.id,
            "text": user_inst.text,
            "reply_markup": json.dumps(user_inst.keyboard),
        },
    )


def getUser(id, username):
    if JsonHelper.userExist(id):
        return User(data=JsonHelper.getUserJson(id))
    return createUser(id, username)


def createUser(id, username):
    data = {
        "id": id,
        "state": userState.BEGIN.value,
        "username": username,
        "result": False,
    }
    JsonHelper.writeUserJson(id, data)
    return User(data=JsonHelper.getUserJson(id))


def ProcessMessage(msg):
    # TODO: Hide msg parser in another module
    id = msg["from"]["id"]
    username = msg["from"]["first_name"]
    if msg["from"].get("last_name", None) is not None:
        username += " " + msg["from"]["last_name"]
    message = msg["text"]

    # this needs to avoid handling start message from all states
    user = getUser(id, username)
    if user.state != userState.BEGIN and message == tgCommand.START.value:
        user.state = userState.BEGIN

    user.changeState(user.stateHandler(message))
