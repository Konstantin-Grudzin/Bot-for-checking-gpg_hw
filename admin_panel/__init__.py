from sql_helper import SQL
from secret_info import ADMIN_TELEGRAM_ID
import tg_handler


def notify():
    sql = SQL()
    new_user, name, group = sql.get_new_passed_user()
    if new_user is None:
        return
    tg_handler.send_text(ADMIN_TELEGRAM_ID, f"{name} {group} pass the exam, hooray!")
    sql.set_user(new_user)
