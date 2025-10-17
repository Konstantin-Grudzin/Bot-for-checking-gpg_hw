from json_helper import JSON
from sql_helper import SQL
from secret_info import ADMIN_TELEGRAM_ID
import tg_handler


def notify():
    json_data = JSON()
    old_user = json_data.get_user()
    sql = SQL()
    new_user, name, group = sql.get_new_passed_user(old_user)
    if new_user is None:
        return
    tg_handler.send_text(ADMIN_TELEGRAM_ID, f"{name,group} pass the exam, hooray!")
    json_data.set_user(new_user)
