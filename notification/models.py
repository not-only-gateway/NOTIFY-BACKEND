from sqlalchemy.exc import SQLAlchemyError
from app import db
from sqlalchemy.types import ARRAY
from sqlalchemy.sql import func


class Notification(db.Model):
    __tablename__ = 'notificacao'

    id = db.Column('codigo_id', db.BigInteger, primary_key=True)
    title = db.Column('titulo', db.String, nullable=False)
    message = db.Column('mensagem', db.String)
    footer = db.Column('rodape', db.String)
    sender = db.Column('remetente', db.String, nullable=False)
    receiver = db.Column('destinatario', db.String, nullable=False)
    seen = db.Column('visto', db.Boolean, nullable=False, default=False)
    seen_on = db.Column('visto_em', db.DateTime, default=None, onupdate=func.now())
    files = db.Column('arquivos', ARRAY(db.String))
    creation_date = db.Column('data_de_criação', db.DateTime, nullable=False, server_default=func.now())

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
