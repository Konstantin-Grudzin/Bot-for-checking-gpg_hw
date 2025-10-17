from enum import Enum


class UserState(Enum):
    BEGIN = 0
    ENTER_ADMIN = 12
    ADMIN = 18
    WAIT_FOR_GPG = 50
    USER_CHECK_GPG = 51
    WAIT_FOR_CORRECT_MESSAGE = 52


class TgCommand(Enum):
    START = "/start"
    BEGIN_EXAM = "Начать зачёт"
    BECOME_ADMIN = "Стать админом"
    PRINT_ALL_PASSED = "Вывести список сдавших"
    EXIT = "Выход"
    OK = "OK"
    NO = "Нет"


menu_text = {
    UserState.BEGIN: "Добро пожаловать на начальную страницу: тут ты можешь:\n1.Сдать зачёт\n2.Войти в админ-панель",
    UserState.ENTER_ADMIN: "Проверяю, достоен ли ты войти...",
    UserState.WAIT_FOR_GPG: "Жду твой gpg-ключ\nВ имени ключа укажи своё имя, а в комментах - свою группу\nОн должен быть типа RSA(1), длиной 4096 байт\nПодсказка: получить его можно с помощью этих комманд:\n<code>gpg --full-gen-key</code>\n<code>gpg --export -a bob@example.com > bob_public.gpg</code>\nМожешь пислать его ввиде текста, или же файлом",
    UserState.USER_CHECK_GPG: "Проверь, правильно ли ты указал данные?\n(Внимание! Имменно они будут отправлены преподавателю, потом изменить их нельзя!)",
    UserState.WAIT_FOR_CORRECT_MESSAGE: "Я зашифровал сообщение, скопируй его, расшифруй и отправь мне\nПодсказка:\nВоспользуйся командой\n<code>gpg -d -o message.txt 'имя файла с этим сообщением'</code>",
}

menu_buttons = {
    UserState.BEGIN: [
        [TgCommand.BEGIN_EXAM.value],
        [TgCommand.BECOME_ADMIN.value],
    ],
    UserState.ADMIN: [
        [TgCommand.EXIT.value],
    ],
    UserState.USER_CHECK_GPG: [[TgCommand.OK.value,TgCommand.NO.value],
                               [TgCommand.EXIT.value]
    ],
    UserState.WAIT_FOR_GPG: [[TgCommand.EXIT.value]],
    UserState.WAIT_FOR_CORRECT_MESSAGE: [[TgCommand.EXIT.value]],
}


def gen_start_text(user):
    return f"Привет, добро пожаловать в автоматический зачётник по gpg!\nТвоё имя сейчас:{user.username}\nБот сделан @groks27"


def success_name_changing(user):
    return f"Имя изменено!\nТеперь ты {user.username}"

def check_you_info(user):
    return f"Имя:{user.name}\nГруппа:{user.group}\nПроверь внимательно, потом изменить это будет нельзя!"


wrong_command = "Прости, но ты ввёл неправильную команду"
your_gpg_key_delete = "Прости, но твой gpg-ключ был удалён"
your_gpg_added = "Твой gpg ключ в системе!"
incorrect_gpg = (
    "Прости, но твой gpg ключ, не получилось добавить в систему, попробуй новый ключ"
)
you_are_correct = (
    "Поздравляю, ты ответил верно! Отметка о твоём зачёте уже летит преподователю!"
)
incorrect_message = "Прости, но это неправильная расшифровка, попробуй ещё раз"
admin_notify_on = "уВЕДомления включены"
admin_notify_off = "уВЕДомления выключены"
