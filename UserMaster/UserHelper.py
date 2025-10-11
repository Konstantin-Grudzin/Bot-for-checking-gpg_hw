from enum import Enum


class UserState(Enum):
    BEGIN = 0
    ENTER_ADMIN = 12
    ADMIN = 18
    CHANGE_NAME = 25
    WAIT_FOR_GPG = 50
    WAIT_FOR_CORRECT_MESSAGE = 51


class TgCommand(Enum):
    START = "/start"
    CHANGE_NAME = "Изменить Имя"
    BEGIN_EXAM = "Начать зачёт"
    BECOME_ADMIN = "Стать админом"
    ADMIN_NOTIFY_ON = "Включить уведомления админа"
    ADMIN_NOTIFY_OFF = "Выключить уведомления админа"
    EXIT = "Выход"


menuText = {
    UserState.BEGIN: "Добро пожаловать на начальную страницу: тут ты можешь:\n1.Сдать зачёт\n2.Изменить имя, под которым уведомление о зачёте будет отправлено преподавателю (Изначально берётся из имени в тг)\n3.Войти в админ-панель",
    UserState.ENTER_ADMIN: "Введи пасс-ключ для входа в админ панель",
    UserState.ADMIN: "",
    UserState.CHANGE_NAME: "Напиши новое ФИ и группу через пробел (Учти, его нельзя изменить после и во время получения зачёта!):\n",
    UserState.WAIT_FOR_GPG: "Жду твой gpg-ключ\nПодсказка: получить его можно с помощью этих комманд:\n<code>gpg --full-gen-key</code>\n<code>gpg --export -a bob@example.com > bob_public.gpg</code>",
    UserState.WAIT_FOR_CORRECT_MESSAGE: "Я зашифровал сообщение, скопируй его, расшифруй и отправь мне\nПодсказка:\nВоспользуйся командой\n<code>gpg -d -o message.txt 'имя файла с этим сообщением'</code>",
}

menuButtons = {
    UserState.BEGIN: [
        [TgCommand.BEGIN_EXAM.value, TgCommand.CHANGE_NAME.value],
        [TgCommand.BECOME_ADMIN.value],
    ],
    UserState.ENTER_ADMIN: [[TgCommand.EXIT.value]],
    UserState.ADMIN: [
        [TgCommand.ADMIN_NOTIFY_ON.value],
        [TgCommand.ADMIN_NOTIFY_OFF.value],
        [TgCommand.EXIT.value],
    ],
    UserState.CHANGE_NAME: [[TgCommand.EXIT.value]],
    UserState.WAIT_FOR_GPG: [[TgCommand.EXIT.value]],
    UserState.WAIT_FOR_CORRECT_MESSAGE: [[TgCommand.EXIT.value]],
}


def gen_start_text(user):
    return f"Привет, добро пожаловать в автоматический зачётник по gpg!\nТвоё имя сейчас:{user.username}\nБот сделан @groks27"


def success_name_changing(user):
    return f"Имя изменено!\nТеперь ты {user.username}"


wrong_command = "Прости, но ты ввёл неправильную команду"
wrong_admin_data = "Прости, но тебя нет в списках админов"
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
