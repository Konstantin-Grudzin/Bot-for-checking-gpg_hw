import JsonHelper
from UserMaster.User import User
from UserMaster.UserHelper import UserState, TgCommand


def get_user(id, username):
    if JsonHelper.user_exist(id):
        return User(data=JsonHelper.get_user_json(id))
    return create_user(id, username)


def create_user(id, username):
    data = {
        "id": id,
        "state": UserState.BEGIN.value,
        "username": username,
        "result": False,
    }
    JsonHelper.write_user_json(id, data)
    return User(data=JsonHelper.get_user_json(id))


def process_message(msg):
    # TODO: Hide msg parser in another module
    id = msg["from"]["id"]
    username = msg["from"]["first_name"]
    if msg["from"].get("last_name", None) is not None:
        username += " " + msg["from"]["last_name"]
    message = msg["text"]

    # this needs to avoid handling start message from all states
    user = get_user(id, username)
    if user.state != UserState.BEGIN and message == TgCommand.START.value:
        user.state = UserState.BEGIN

    user.change_state(user.state_handler(message))
