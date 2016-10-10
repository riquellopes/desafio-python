import os
import jwt
import hashlib
from datetime import datetime
from app.db import db
from sqlalchemy import event
from app.exceptions import ExceptionCloseTime


def jwt_encode(email):
    return jwt.encode({"email": email}, os.environ.get("DESAFIO_SECRET_KEY"), algorithm='HS256').strip()

str_token = lambda token: bytes(token, "ascii")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    modified = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.now())
    token = db.Column(db.String(200), unique=True)
    phones = db.relationship('Phone', backref="user", lazy='dynamic')

    def to_authorize(self):
        user = db.session.query(User).filter(User.email == self.email).first()

        if user is None:
            raise Exception("Usuário e/ou senha inválidos")

        if not self._check_password(user.password, self.password):
            raise Exception("Usuário e/ou senha inválidos")
        return user

    @classmethod
    def to_encrypt(cls, password):
        return hashlib.sha1(password.encode()).hexdigest()

    def _check_password(self, upassword, password):
        if not self.id:
            password = self.to_encrypt(password)
        return upassword == password

    def update_last_login(self):
        self.last_login = db.func.current_timestamp()
        db.session.merge(self)
        db.session.commit()

    @classmethod
    def find_by_token(cls, token):
        token = str_token(token)
        return db.session.query(User).filter(User.token == token).one()

    def is_valid_login(self):
        if abs((datetime.now() - self.last_login).total_seconds() / 60.0) > 30:
            raise ExceptionCloseTime("Tempo encerrado.")
        return True


@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, instance):
    instance.password = instance.to_encrypt(instance.password)
    instance.token = jwt_encode(instance.email)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(9))
    ddd = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
