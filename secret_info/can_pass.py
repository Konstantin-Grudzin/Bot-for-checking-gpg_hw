from secret_info import ADMIN_TELEGRAM_ID


def can_pass(admin_id):
    return admin_id == ADMIN_TELEGRAM_ID
