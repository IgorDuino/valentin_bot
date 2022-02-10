from russiannames.parser import NamesParser
from tools.valentins import ValentineCard
import PIL


russian_name_parser = NamesParser()


def generate_valentine_image(valentin: ValentineCard):
    # TODO: do picture generation
    pass


def generate_link(uid) -> str:
    return f'https://t.me/valentinkin_bot?start={uid}'


def get_tg_id_by_code(code):
    return code


def get_gender_by_full_name(full_name):
    parsed_name = russian_name_parser.parse(full_name)
    gender = parsed_name.get('gender')
    if gender == 'm':
        return True
    else:
        return False
