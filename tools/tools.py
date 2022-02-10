from russiannames.parser import NamesParser

russian_name_parser = NamesParser()


def get_gender_by_full_name(full_name):
    parsed_name = russian_name_parser.parse(full_name)
    gender = parsed_name.get('gender')
    if gender == 'm':
        return True
    else:
        return False
