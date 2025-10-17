from pathlib import Path
import re

import gnupg
from faker import Faker

from sql_helper import SQL

fake = Faker()
gpg = gnupg.GPG(gnupghome="gpg")

currLoc = [*Path(__file__).parents][1] / "user_text"

FIO_REGEX = re.compile(r"^[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?\s[А-ЯЁ]\.[А-ЯЁ]\.$")


def gen_some_text():
    return fake.name()


def parse_uid(uid: str):
    """
    Разбирает UID вида:
      - "Full Name (comment) <email>"
      - "Full Name <email>"
      - "Full Name (comment)"
      - "Full Name"
    Возвращает (name, comment) — comment может быть None.
    """
    comment = None
    m = re.search(r"\((.*?)\)", uid)
    if m:
        comment = m.group(1).strip()

    # вырежем <email> и (comment)
    # оставим только имя (trim)
    name = re.sub(r"<.*?>", "", uid)  # удалить email
    name = re.sub(r"\(.*?\)", "", name)  # удалить комментарий
    name = name.strip()
    if not name:
        name = None

    return name, comment


def get_key_info_by_fingerprint(fingerprint: str):
    """
    Ищет ключ по fingerprint в публичных и секретных ключах.
    Возвращает dict:
      {
        "fingerprint": "...",
        "algo": "...",        # например "RSA"
        "length": 4096,       # int (если есть)
        "name": "Full Name" | None,
        "comment": "..." | None,
        "uids": [...],        # оригинальные UIDы
        "is_secret": True|False
      }
    Если ключ не найден — возвращает None.
    """
    if not fingerprint:
        return None

    search_lists = [
        (gpg.list_keys(), False),
        (gpg.list_keys(secret=True), True),
    ]

    fpr_lower = fingerprint.lower()
    for keys, is_secret in search_lists:
        for key in keys:
            key_fpr = key.get("fingerprint") or key.get("fingerprints")
            if isinstance(key_fpr, (list, tuple)):
                key_fp_list = [str(x).lower() for x in key_fpr]
                matches = fpr_lower in key_fp_list
            else:
                matches = str(key_fpr).lower() == fpr_lower

            if matches:
                algo = (
                    key.get("algo")
                    or key.get("key_type")
                    or key.get("keytype")
                    or key.get("type")
                )
                length_raw = (
                    key.get("length") or key.get("keylength") or key.get("key_size")
                )
                try:
                    length = int(length_raw) if length_raw is not None else None
                except (ValueError, TypeError):
                    length = None

                uids = key.get("uids") or key.get("uid") or []
                first_uid = uids[0] if uids else None
                name, comment = (None, None)
                if first_uid:
                    name, comment = parse_uid(first_uid)

                return {
                    "fingerprint": fingerprint,
                    "algo": int(algo),
                    "length": length,
                    "name": name,
                    "comment": comment,
                    "uids": uids,
                    "is_secret": bool(is_secret),
                }

    return None


def delete_gpg(id):
    sql = SQL()
    fp = sql.get_fingerprint(id)
    gpg.delete_keys(fp)
    path = Path(currLoc / f"{id}.txt")
    if path.exists():
        path.unlink()


def check_format(fio):
    if not isinstance(fio, str):
        return False
    fio = fio.strip()
    return bool(FIO_REGEX.fullmatch(fio))


def add_gpg(id, message):
    sql = SQL()
    try:
        import_k = gpg.import_keys(message)
    except Exception:
        return "You key is corrupted!"

    # TODO add error keys and say's thats wrong?
    key = get_key_info_by_fingerprint(import_k.fingerprints[0])
    if key["algo"] != 1:
        return "Algo of your key must be RSA(1)"
    if key["length"] != 4096:
        return "Length of your algo must be 4096"
    if key["is_secret"]:
        return "Your key must be public"
    if key["name"] is None or check_format(key["name"]):
        return "Wrong format of name"
    if key["comment"] is None:
        return "Comment connot be empty"
    if import_k.fingerprints:
        sql.set_fingerprint(id, import_k.fingerprints[0])
        with open(currLoc / f"{id}.txt", "w") as file:
            file.write(gen_some_text())
        return None
    return "You key is corrupted!"


def get_info_from_key(id):
    sql = SQL()
    fp = sql.get_fingerprint(id)
    key = get_key_info_by_fingerprint(fp)
    print(key["name"], key["comment"])
    return key["name"], key["comment"]


def get_message(id):
    sql = SQL()
    fp = sql.get_fingerprint(id)
    with open(currLoc / f"{id}.txt", "rb") as file:
        encrypted = gpg.encrypt_file(file, fp, always_trust=True)
    if not encrypted.ok:
        print("Encypted Error:", encrypted.stderr)
    return str(encrypted)


def get_dec_message(id):
    with open(currLoc / f"{id}.txt", "r") as file:
        return file.read()
