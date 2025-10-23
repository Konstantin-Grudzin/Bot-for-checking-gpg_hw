from pathlib import Path
import time
import admin_panel
from sql_helper import SQL
import tg_handler
from observer.dispatcher import Dispatcher

path = Path(__file__)


def init() -> None:
    path.parent.touch("data.db")
    SQL(path.parent / "data.db")


def main() -> None:
    print("===start===")
    dispatcher = Dispatcher()
    try:
        while True:
            for message in tg_handler.get_updates():
                print(message)
                dispatcher(message)
            admin_panel.notify()
            print("===HeartBeat===")
            time.sleep(0.5)
    except KeyboardInterrupt:
        SQL().close()


if __name__ == "__main__":
    init()
    main()
