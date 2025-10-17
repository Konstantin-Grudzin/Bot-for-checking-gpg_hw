import os

from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID")
ADRESS = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"
DOWNLOAD_ADRESS = "https://api.telegram.org/file/bot" + TELEGRAM_TOKEN + "/"
