import sqlalchemy
from sqlalchemy.orm import relationship
from db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import db_session


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    first_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    second_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    full_name = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    from_cards = relationship("ValentineCard", back_populates='from_user', foreign_keys='ValentineCard.from_user_id')
    to_cards = relationship("ValentineCard", back_populates='to_user', foreign_keys='ValentineCard.to_user_id')

    def __repr__(self):
        return f'User tg_id - {self.tg_id}'


def get_users_valentins(tg_id):
    pass


def get_user_by_id(tg_id: int | str) -> User | bool:
    tg_id = int(tg_id)
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user if user else False


def create_user(uid, username=None, first_name=None, second_name=None, full_name=None, sex=None) -> User:
    user = User()
    user.tg_id = uid
    user.username = username
    user.first_name = first_name
    user.second_name = second_name
    user.full_name = full_name
    user.sex = sex

    session = db_session.create_session()
    session.add(user)
    session.commit()

    return get_user_by_id(uid)


def is_set_user(uid):
    return get_user_by_id(uid) == False
