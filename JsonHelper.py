import json
import os
from pathlib import Path


path = Path(__file__)
default_path = str(path.parent) + ("/user/")


def createFile(data, loc):
    with open(loc, "w") as file:
        txt = json.dumps(data, indent=4)
        file.write(txt)


def rewrite_file(data, file):
    txt = json.dumps(data, indent=4)
    file.truncate(0)
    file.seek(0)
    file.write(txt)


def user_exist(id):
    return os.path.exists(default_path + f"{id}.json")


def get_user_json(id):
    with open(default_path + f"{id}.json", "r") as file:
        return json.load(file)


def write_user_json(id, data):
    with open(default_path + f"{id}.json", "w") as file:
        rewrite_file(data, file)


def change_state(id, state):
    with open(default_path + f"{id}.json", "r+") as file:
        data = json.load(file)
        data["state"] = state.value
        rewrite_file(data, file)


def change_name(id, name):
    with open(default_path + f"{id}.json", "r+") as file:
        data = json.load(file)
        data["username"] = name
        rewrite_file(data, file)


def change_result(id):
    with open(default_path + f"{id}.json", "r+") as file:
        data = json.load(file)
        data["result"] = True
        rewrite_file(data, file)
