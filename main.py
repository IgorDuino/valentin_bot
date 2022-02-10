import telebot

import menu
import secret
import texts
import time
import db_session
from tools.users import User, create_user, get_user_by_tg_id
from tools.valentins import ValentineCard, create_valentine
from tools.tools import *
import tools.qrcode_tools

db_session.global_init("db.sqlite")

bot = telebot.TeleBot(secret.tg_token)

temp_valentins = {}


def create_new_valentine_text(message: telebot.types.Message):
    valentine: ValentineCard = temp_valentins.get(message.from_user.id)
    if valentine is None:
        bot.edit_message_text(texts.simple_error,
                              message.from_user.id,
                              message.id)
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        return
    valentine.text = message.text
    msg = bot.edit_message_text(texts.second_step_new_valentine,
                                message.from_user.id,
                                message.id)

    bot.register_next_step_handler(msg, create_new_valentine_background)


def create_new_valentine_background(message: telebot.types.Message):
    valentine: ValentineCard = temp_valentins.get(message.from_user.id)
    if valentine is None:
        bot.send_message(message.from_user.id,
                         'Ошибочка :(\nПерезапусти меня - /start или открой ссылку друга(подруги) заного')
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        return

    valentine.background = int(message.text)
    msg = bot.edit_message_text(texts.third_step_new_valentine(valentine),
                                message.from_user.id,
                                message.id,
                                reply_markup=menu.is_correct_valentine()
                                )


@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
    text = message.text
    uid = int(message.from_user.id)

    code = text.split('/start')[1]

    user = get_user_by_tg_id(uid)

    if not user:
        username = message.from_user.username
        first_name = message.from_user.first_name
        second_name = message.from_user.last_name
        full_name = message.from_user.full_name

        user = create_user(uid, username, first_name, second_name, full_name)

    if code:
        to_user_tg_id = get_tg_id_by_code(code)
        to_user = get_user_by_tg_id(to_user_tg_id)
        if to_user:
            bot.send_message(user.tg_id,
                             texts.welcome_invite_text(user.first_name, to_user.first_name, to_user.gender),
                             reply_markup=menu.invite_menu(to_user)
                             )
        else:
            bot.send_message(user.tg_id, texts.welcome_text(user.first_name, user.link))

    else:
        bot.send_message(user.tg_id, texts.welcome_text(user.first_name, user.link))


@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    uid = message.chat.id
    user = get_user_by_tg_id(uid)

    bot.send_message(user.tg_id, 'help')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
    if call.data.startswith('send_valentin_'):
        is_anonymous = 'anonymous' in call.data

        from_user = get_user_by_tg_id(call.from_user.id)
        to_user = get_user_by_tg_id(call.data.split('_')[-1])

        new_valentine = ValentineCard()
        new_valentine.to_user_id = to_user.id
        new_valentine.is_anonymous = is_anonymous
        new_valentine.from_user_id = from_user.id

        temp_valentins[from_user.tg_id] = new_valentine

        msg = bot.send_message(from_user.tg_id,
                               texts.first_step_new_valentine)

        bot.register_next_step_handler(msg, create_new_valentine_text)

    elif call.data == 'correct_valentine':
        valentine = temp_valentins.get(call.from_user.id)
        if valentine is None:
            bot.edit_message_text(texts.simple_error,
                                  call.from_user.id,
                                  call.message.id)
            return
        if create_valentine(valentine):
            bot.send_message(call.from_user.id,
                             texts.success_send)

    elif call.data == 'incorrect_valentine':
        pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            delay = 3
            text = f'Error: {e}, restarting after {delay} seconds'
            print(text)
            bot.send_message(secret.admin_id, text)
            time.sleep(delay)
            text = f'Restarted'
            print(text)
            bot.send_message(secret.admin_id, text)
