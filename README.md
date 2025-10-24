# Telegram Bot for checking students' skills of using gpg

Disclaimer: this bot was targeted for russian students/ If you wnat to use it in another languages, use translation (Maybe i add translation in future? We will see)

This bot get some functions
1. You can add gpg key and try to decrypt message that bot gives you
2. If you are teacher, you can go to admin mode and get new passed students' names

### How to install it
1. Clone repo
2. make a new venv
3. Install dependencies from `requirements.txt`
4. In `secret_info` create `.env` file and fill it with bot token and admin id (see `example.env` in source `secret_info` dir)
5. go to source dir and use command `python3 .`
6. ???
7. Profit!

### Little user guide about admin (because it don't have much description in tg):
When the admin press start in bot, it will get notifications of passed students. 
And it can get all passed students by pressing special button.

Good luck, `comrade` :)
