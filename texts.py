from tools.valentins import ValentineCard


def welcome_invite_text(name, referal_name, gender):
    text = f"♥️♥️♥️Привет, {name}! ♥️♥️♥️\nЯ бот для обмена валентинками\nЯ вижу ты открыл меня по ссылке от " \
           f"{referal_name}, ты хочешь отправить {'ему' if gender else 'ей'} валентинку?"
    return text


def welcome_text(name, link):
    text = f"♥️♥️♥️Привет, {name}! ♥️♥️♥️\nЯ бот для обмена валентинками. Вот твоя ссылка - {link}"
    return text


yes_send_anonymous = "Да, отправить анонимно ❤🐱‍💻"
yes_send_public = "Да, отправить НЕ анонимно ❤"
no_open_main_menu = "Нет, открыть главное меню"
first_step_new_valentine = 'Отправь текст открытки 📓'
second_step_new_valentine = 'Выбери фон (1-3)'

correct_valentine = 'Да, всё отлично'
incorrect_valentine = 'Не, фигня. Давай по новой!'

success_send = 'Твоя валентинка была записана и 14го февраля она придет ей(ему). Желаю тебе удачи :)'

simple_error = 'Ошибочка :(\nПерезапусти меня - /start или открой ссылку друга(подруги) заного'


def third_step_new_valentine(valentine: ValentineCard) -> str:
    return f'Отлично, смотри как получилось\n' \
           f'{valentine.text}'
