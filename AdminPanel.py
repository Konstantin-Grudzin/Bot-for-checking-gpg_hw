import TgHandler

dataJson = None


def set_data(obj):
    global dataJson
    dataJson = obj


def notify():
    if len(dataJson["Admins"]) == 0 or len(dataJson["Good Students"]) == 0:
        return
    admins = dataJson["Admins"]
    stud = dataJson["Good Students"][-1]

    all_sleep = True
    for [admin, allow] in admins.items():
        if not allow:
            continue
        all_sleep = False
        TgHandler.send_text(admin, f"{stud} pass the test,hooray!")
    if not all_sleep:
        dataJson["Good Students"].pop()


def add_good_student(username):
    dataJson["Good Students"].append(username)


def add_admin(id):
    dataJson["Admins"][str(id)] = False


def del_admin(id):
    del dataJson["Admins"][str(id)]


def on_notify(id):
    dataJson["Admins"][str(id)] = True


def off_notify(id):
    dataJson["Admins"][str(id)] = False
