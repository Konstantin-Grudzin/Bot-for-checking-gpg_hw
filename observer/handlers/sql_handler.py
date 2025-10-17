import json
import message_parser
from observer.handlers.handler import Handler
from sql_helper import SQL


class SqlHandler(Handler):
    def can_handle(self, message: dict) -> bool:
        return True

    def handle(self, message: dict) -> bool:
        sql = SQL()
        sql.insert_message(
            message_parser.get_id(message),
            json.dumps(message, indent=2, ensure_ascii=False),
        )
        return True
