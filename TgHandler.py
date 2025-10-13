import json
import requests
from secret_info import address, download_adress


def get_file(file_id):
    resp = requests.get(address + "getFile", params={"file_id": file_id})
    resp = resp.json()
    path = resp["result"]["file_path"]
    resp = requests.get(download_adress + "/" + path)
    return resp.content


def get_updates(offset: int):
    resp = requests.get(address + "getUpdates", params={"offset": offset})
    jsonObj = resp.json()

    if len(jsonObj["result"]):
        offset = jsonObj["result"][-1]["update_id"] + 1
    return [jsonObj, offset]


def send_text(id, text, keyboard=None):
    reply_markup = {
        "keyboard": keyboard,
        "resize_keyboard": True,  # optional: make buttons smaller
        "one_time_keyboard": True,  # optional: keep keyboard after click
    }
    if not text and (keyboard is not None):
        requests.post(
            address + "sendMessage",
            params={
                "chat_id": id,
                "text": "ㅤ",
                "reply_markup": json.dumps(reply_markup),
            },
        )
    if keyboard is None:
        requests.post(address + "sendMessage", params={"chat_id": id, "text": text})
    else:
        requests.post(
            address + "sendMessage",
            params={
                "chat_id": id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(reply_markup),
            },
        )


def send_gpg_message(id, text, keyboard=None):
    print(keyboard)
    if keyboard is None:
        requests.post(
            address + "sendMessage",
            params={
                "chat_id": id,
                "text": "```\n" + text + "\n```",
                "parse_mode": "MarkdownV2",
            },
        )
