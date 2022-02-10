import telebot
import secret
import texts
import time
import db_session
from tools.users import User, create_user, get_user_by_id
from tools.valentins import ValentineCard
from tools.tools import *


db_session.global_init("db.sqlite")

bot = telebot.TeleBot(secret.tg_token)


@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
    text = message.text
    uid = int(message.from_user.id)

    code = text.split('/start')[1]

    user = get_user_by_id(uid)

    if not user:
        username = message.from_user.username
        first_name = message.from_user.first_name
        second_name = message.from_user.last_name
        full_name = message.from_user.full_name
        sex = get_gender_by_full_name(full_name)
        user = create_user(uid, username, first_name, second_name, full_name, sex)

    if code:
        to_user = get_user_by_id(code)
        if to_user:
            bot.send_message(user.tg_id, texts.welcome_invite_text(user.first_name, to_user.first_name))
        else:
            bot.send_message(user.tg_id, texts.welcome_text(user.first_name, 'link'))

    else:
        bot.send_message(user.tg_id, texts.welcome_text(user.first_name, 'link'))


@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    uid = message.chat.id
    user = get_user_by_id(uid)

    bot.send_message(user.tg_id, 'help')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
    # while True:
        # try:
        #     bot.polling(none_stop=True)
        # except Exception as e:
        #     delay = 3
        #     text = f'Error: {e}, restarting after {delay} seconds'
        #     print(text)
        #     bot.send_message(secret.admin_id, text)
        #     time.sleep(delay)
        #     text = f'Restarted'
        #     print(text)
        #     bot.send_message(secret.admin_id, text)
