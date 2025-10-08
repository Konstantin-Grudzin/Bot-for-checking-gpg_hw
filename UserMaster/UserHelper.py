
from enum import Enum


class userState(Enum):
    BEGIN = 0
    ENTER_ADMIN = 12
    ADMIN = 18
    CHANGE_NAME = 25
    WAIT_FOR_GPG=50
    WAIT_FOR_CORRECT_MESSAGE=51

class tgCommand(Enum):
    START = "/start"
    CHANGE_NAME = "Изменить Имя"
    BEGIN_EXAM = "Начать зачёт"
    BECOME_ADMIN = "Стать админом"
    ADMIN_NOTIFY_ON = "Включить уведомления админа"
    ADMIN_NOTIFY_OFF = "Выключить уведомления админа"
    EXIT = "Выход"

menuText =\
{
    userState.BEGIN:"Добро пожаловать на начальную страницу: тут ты можешь:\n1.Сдать зачёт\n2.Изменить имя, под которым уведомление о зачёте будет отправлено преподавателю (Изначально берётся из имени в тг)\n3.Войти в админ-панель",
    userState.ENTER_ADMIN:"Введи пасс-ключ для входа в админ панель",
    userState.ADMIN:"",
    userState.CHANGE_NAME:"Напиши новое ФИ и группу через пробел (Учти, его нельзя изменить после и во время получения зачёта!):\n",
    userState.WAIT_FOR_GPG:"Жду твой gpg-ключ\nПодсказка: получить его можно с помощью этих комманд:\n<code>gpg --full-gen-key</code>\n<code>gpg --export -a bob@example.com > bob_public.gpg</code>",
    userState.WAIT_FOR_CORRECT_MESSAGE:"Я зашифровал сообщение, скопируй его, расшифруй и отправь мне\nПодсказка:\nВоспользуйся командой\n<code>gpg -d -o message.txt 'имя файла с этим сообщением'</code>",
}

menuButtons=\
{
    userState.BEGIN:[[tgCommand.BEGIN_EXAM.value,tgCommand.CHANGE_NAME.value],[tgCommand.BECOME_ADMIN.value]],
    userState.ENTER_ADMIN:[[tgCommand.EXIT.value]],
    userState.ADMIN:[[tgCommand.ADMIN_NOTIFY_ON.value],
                     [tgCommand.ADMIN_NOTIFY_OFF.value],
                     [tgCommand.EXIT.value]],
    userState.CHANGE_NAME:[[tgCommand.EXIT.value]],
    userState.WAIT_FOR_GPG:[[tgCommand.EXIT.value]],
    userState.WAIT_FOR_CORRECT_MESSAGE:[[tgCommand.EXIT.value]],
}

def gen_start_text(user):
    return f"Привет, добро пожаловать в автоматический зачётник по gpg!\nТвоё имя сейчас:{user.username}\nБот сделан @groks27"

def success_name_changing(user):
    return f"Имя изменено!\nТеперь ты {user.username}"

wrong_command = "Прости, но ты ввёл неправильную команду"
wrong_admin_data = "Прости, но тебя нет в списках админов"
your_gpg_key_delete = "Прости, но твой gpg-ключ был удалён"
your_gpg_added = "Твой gpg ключ в системе!"
incorrect_gpg = "Прости, но твой gpg ключ, не получилось добавить в систему, попробуй новый ключ"
you_are_correct = "Поздравляю, ты ответил верно! Отметка о твоём зачёте уже летит преподователю!"
incorrect_message = "Прости, но это неправильная расшифровка, попробуй ещё раз"
admin_notify_on = "уВЕДомления включены"
admin_notify_off = "уВЕДомления выключены"