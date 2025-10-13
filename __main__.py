from pathlib import Path
import json
import AdminPanel
import JsonHelper
import TgHandler
from UserMaster.UserMaster import process_message, process_file

path = Path(__file__)
dataLoc = str(path.parent) + ("/data.json")


def init():
    # create data.json
    if not Path(dataLoc).exists():
        data = {"offset": 0, "Admins": {}, "Good Students": []}
        JsonHelper.create_file(data, dataLoc)

    # create gpg_keys
    Path(str(path.parent) + ("/gpg_keys")).mkdir(exist_ok=True)

    # create user
    Path(str(path.parent) + ("/user")).mkdir(exist_ok=True)


def main():
    print("===start===")
    with open(dataLoc, "r+") as file:
        dataJson = json.load(file)
        AdminPanel.set_data(dataJson)
        while True:
            [messages, dataJson["offset"]] = TgHandler.get_updates(dataJson["offset"])
            for message in messages["result"]:
                print(message)
                messageType = [*message.keys()][1]
                message = message[messageType]
                if message.get("text", None) is not None:
                    process_message(message)
                elif message.get("document", None) is not None:
                    process_file(message)
                else:
                    print("I can't handle this")

            # TODO: Enable SIGKILL message and move this block from while
            AdminPanel.notify()
            JsonHelper.rewrite_file(dataJson, file)
            print("===HeartBeat===")


if __name__ == "__main__":
    init()
    main()
