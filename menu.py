from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(a=False):
    if a:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text="Да, отправить анонимно ❤🐱‍💻", callback_data="send_valentin_anonymous"))
        keyboard.add(
            InlineKeyboardButton(text="Да, отправить НЕ анонимно ❤", callback_data="send_valentin_public"))
        keyboard.add(
            InlineKeyboardButton(text="Нет, открыть главное меню", callback_data="main_menu"))

        return keyboard
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text="Моя ссылка", callback_data="my_link"))
        keyboard.add(
            InlineKeyboardButton(text="Да, отправить НЕ анонимно ❤", callback_data="send_valentin_public"))
        keyboard.add(
            InlineKeyboardButton(text="Нет, открыть главное меню", callback_data="main_menu"))

        return keyboard