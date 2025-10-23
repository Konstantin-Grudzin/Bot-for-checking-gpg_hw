import json
import requests
from secret_info import ADDRESS, DOWNLOAD_ADDRESS, ADMIN_TELEGRAM_ID
from sql_helper import SQL


def get_file(file_id):
    resp = requests.get(ADDRESS + "getFile", params={"file_id": file_id})
    resp = resp.json()
    path = resp["result"]["file_path"]
    resp = requests.get(DOWNLOAD_ADDRESS + "/" + path)
    return resp.content


offset = 0


def get_updates():
    global offset
    resp = requests.get(ADDRESS + "getUpdates", params={"offset": offset})
    jsonObj = resp.json()

    if len(jsonObj["result"]):
        offset = jsonObj["result"][-1]["update_id"] + 1
    return jsonObj["result"]


def send_text(id, text=None, keyboard=None):
    reply_markup = {
        "keyboard": keyboard,
        "resize_keyboard": True,  # optional: make buttons smaller
        "one_time_keyboard": True,  # optional: keep keyboard after click
    }
    print(type(text), type(keyboard))
    match text, keyboard:
        case None, list():
            requests.post(
                ADDRESS + "sendMessage",
                params={
                    "chat_id": id,
                    "text": "ㅤ",
                    "reply_markup": json.dumps(reply_markup),
                },
            )
        case str(), None:
            requests.post(ADDRESS + "sendMessage", params={"chat_id": id, "text": text})
        case str(), list():
            requests.post(
                ADDRESS + "sendMessage",
                params={
                    "chat_id": id,
                    "text": text,
                    "parse_mode": "HTML",
                    "reply_markup": json.dumps(reply_markup),
                },
            )
        case _:
            print("skip")
            pass


def send_big_text(id, text):
    requests.post(
        ADDRESS + "sendMessage",
        params={
            "chat_id": id,
            "text": "```\n" + text + "\n```",
            "parse_mode": "MarkdownV2",
        },
    )


def print_all_passed():
    sql = SQL()
    passed = sql.get_list_of_all_passed()
    send_big_text(ADMIN_TELEGRAM_ID, "\n".join(passed))
