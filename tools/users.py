import sqlalchemy
from sqlalchemy.orm import relationship
from db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import db_session
from tools.tools import get_gender_by_full_name, generate_link


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    second_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, unique=False, default=False)
    full_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.Boolean, unique=False, default=False)
    from_cards = relationship("ValentineCard", back_populates='from_user', foreign_keys='ValentineCard.from_user_id')
    to_cards = relationship("ValentineCard", back_populates='to_user', foreign_keys='ValentineCard.to_user_id')

    def __repr__(self):
        return f'User tg_id - {self.tg_id}'


def get_user_by_tg_id(tg_id: int | str) -> User | bool:
    tg_id = int(tg_id)
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user if user else False


def create_user(tg_id, username=None, first_name=None, second_name=None, full_name=None) -> User:
    user = User()
    user.tg_id = tg_id
    user.username = username
    user.link = generate_link(tg_id)
    user.first_name = first_name
    user.second_name = second_name
    user.full_name = full_name
    user.gender = get_gender_by_full_name(full_name)

    session = db_session.create_session()
    session.add(user)
    session.commit()

    return get_user_by_tg_id(tg_id)


def is_set_user(uid):
    return get_user_by_tg_id(uid) == False
