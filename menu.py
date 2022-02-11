from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from tools.users import User
import texts


def invite_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text=texts.yes_send_anonymous, callback_data=f"send_valentin_anonymous_{to_user.tg_id}"))
    keyboard.add(
        InlineKeyboardButton(text=texts.yes_send_public, callback_data=f"send_valentin_public_{to_user.tg_id}"))
    keyboard.add(
        InlineKeyboardButton(text=texts.no_open_main_menu, callback_data="main_menu"))

    return keyboard


def is_correct_valentine() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=texts.correct_valentine, callback_data="correct_valentine"))
    keyboard.add(InlineKeyboardButton(text=texts.incorrect_valentine, callback_data="incorrect_valentine"))

    return keyboard

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=texts.admin_send_all_valentines, callback_data="admin_send_all_valentines"))
    keyboard.add(InlineKeyboardButton(text=texts.close, callback_data="main_menu"))

    return keyboard
