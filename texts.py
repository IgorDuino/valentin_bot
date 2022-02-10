def welcome_invite_text(name, referal_name, sex):
    text = f"♥️♥️♥️Привет, {name}! ♥️♥️♥️\nЯ бот для обмена валентинками\nЯ вижу ты открыл меня по ссылке от " \
           f"{referal_name}, ты хочешь отправить {'ему' if sex else 'ей'} валентинку?"
    return text


def welcome_text(name, link):
    text = f"♥️♥️♥️Привет, {name}! ♥️♥️♥️\nЯ бот для обмена валентинками. Вот твоя ссылка - {link}"
    return text
