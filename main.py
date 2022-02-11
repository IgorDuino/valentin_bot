import telebot
import os
import menu
import secret
import texts
import time
import db_session
from tools.users import User, create_user, get_user_by_tg_id, make_admin, get_all_users
from tools.valentins import ValentineCard, create_valentine, get_all_valentins
from tools.qrcode_tools import generate_qr
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
    msg = bot.send_message(message.from_user.id, texts.second_step_new_valentine, )

    bot.register_next_step_handler(msg, create_new_valentine_background)


def create_new_valentine_background(message: telebot.types.Message):
    valentine: ValentineCard = temp_valentins.get(message.from_user.id)
    if valentine is None:
        bot.edit_message_text(texts.simple_error,
                              message.from_user.id,
                              message.id)
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        return

    valentine.background = int(message.text)
    msg = bot.send_message(message.from_user.id,
                           texts.third_step_new_valentine(valentine),
                           reply_markup=menu.is_correct_valentine())


def add_admin_handler(message: telebot.types.Message):
    find_user = get_user_by_tg_id(message.text)
    if find_user:
        make_admin(find_user)


@bot.message_handler(commands=['admin'])
def admin(message: telebot.types.Message):
    user = get_user_by_tg_id(message.from_user.id)
    if not user.is_admin:
        bot.send_message(user.tg_id, texts.not_admin)
        return

    bot.send_message(user.tg_id, texts.admin, reply_markup=menu.admin_menu())


def first_join(user: User, message: telebot.types.Message):
    file_name = f'img/temp/{user.id}.png'
    generate_qr(user.link, file_name)

    text = texts.welcome_text(user.first_name, user.link)
    bot.send_photo(user.tg_id, open(file_name, 'rb'), text)

    os.remove(file_name)


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
            if user.tg_id == to_user.tg_id:
                bot.send_message(user.tg_id,
                                 texts.self_valentine_error)
                return

            bot.send_message(user.tg_id,
                             texts.welcome_invite_text(user.first_name, to_user.first_name, to_user.gender),
                             reply_markup=menu.invite_menu(to_user))
        else:
            first_join(user, message)

    else:
        first_join(user, message)


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

        msg = bot.edit_message_text(texts.first_step_new_valentine,
                                    from_user.tg_id,
                                    call.message.id)

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
        # Copy data from old valentin
        print(temp_valentins)
        old_valentin: ValentineCard = temp_valentins[call.from_user.id]
        is_anonymous = old_valentin.is_anonymous

        from_user = old_valentin.from_user
        to_user = old_valentin.to_user

        # Remove old valentin
        try:
            del temp_valentins[call.from_user.id]
        except KeyError:
            bot.send_message(call.from_user.id,
                             texts.simple_error)

        # Create new valentin
        new_valentine = ValentineCard()
        new_valentine.to_user_id = to_user.id
        new_valentine.is_anonymous = is_anonymous
        new_valentine.from_user_id = from_user.id

        temp_valentins[from_user.tg_id] = new_valentine

        msg = bot.send_message(from_user.tg_id,
                               texts.first_step_new_valentine)

        bot.register_next_step_handler(msg, create_new_valentine_text)

    elif call.data == 'admin_send_all_valentines':
        valentins = get_all_valentins()
        if len(valentins) == 0:
            bot.edit_message_text('Валентинок нет',
                                  call.from_user.id,
                                  call.message.id,
                                  reply_markup=menu.admin_menu())
            return

        for valentin in valentins:
            valentin: ValentineCard
            to_user: User = valentin.to_user
            bot.send_message(to_user.tg_id,
                             valentin.text)
        bot.edit_message_text('Всё отправили',
                              call.from_user.id,
                              call.message.id)
    # Admins functions
    elif call.data == 'add_new_admin':
        msg = bot.edit_message_text('Введите id пользователя',
                                    call.from_user.id,
                                    call.message.id)
        bot.register_next_step_handler(msg, add_admin_handler)


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
