from pathlib import Path
import gnupg
from faker import Faker

fake = Faker()
gpg = gnupg.GPG()
currLoc = str(Path(__file__).parent) + "/gpg_keys/"


def gen_some_text():
    return fake.name()


def delete_gpg(id):
    path = Path(currLoc + f"{id}.fp")
    if path.exists():
        with path.open("r") as file:
            fp = file.read().strip()
            gpg.delete_keys(fp)
        path.unlink()
    path = Path(currLoc + f"{id}.txt")
    if path.exists():
        path.unlink()


def add_gpg(id, message):
    delete_gpg(id)
    try:
        import_k = gpg.import_keys(message)
    except Exception:
        return False
    if import_k.fingerprints:
        with open(currLoc + f"{id}.fp", "w") as file:
            file.write(import_k.fingerprints[0])
        with open(currLoc + f"{id}.txt", "w") as file:
            file.write(gen_some_text())
        return True
    return False


def get_message(id):
    with open(currLoc + f"{id}.fp", "r") as file:
        fp = file.read().strip()
    with open(currLoc + f"{id}.txt", "rb") as file:
        encrypted = gpg.encrypt_file(file, fp, always_trust=True)
    if not encrypted.ok:
        print("Encypted Error:", encrypted.stderr)
    return str(encrypted)


def get_dec_message(id):
    with open(currLoc + f"{id}.txt", "r") as file:
        return file.read()
