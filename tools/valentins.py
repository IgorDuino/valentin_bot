import sqlalchemy
from sqlalchemy.orm import relationship
from db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import db_session


class ValentineCard(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'valentine_cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    is_anonymous = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    background = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    from_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    from_user = relationship('User', foreign_keys=[from_user_id])
    to_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    to_user = relationship('User', foreign_keys=[to_user_id])

    def __repr__(self):
        return f'User tg_id - {self.tg_id}'


def create_valentine(valentine: ValentineCard) -> bool:
    session = db_session.create_session()
    session.add(valentine)
    session.commit()

    return True
