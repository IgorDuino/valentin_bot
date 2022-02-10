import sqlalchemy
from sqlalchemy.orm import relationship
from db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class ValentineCard(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'valentine_cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    to_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    is_anonymous = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    text = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    background = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    from_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    from_user = relationship('User', foreign_keys=[from_user_id])
    to_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    to_user = relationship('User', foreign_keys=[to_user_id])

    def __repr__(self):
        return f'User tg_id - {self.tg_id}'


