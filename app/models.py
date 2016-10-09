import os
import jwt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from sqlalchemy import event
from app.exceptions import ExceptionCloseTime


def jwt_encode(email):
    return jwt.encode({"email": email}, os.environ.get("DESAFIO_SECRET_KEY"), algorithm='HS256').strip()


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
        user = db.session.query(User).filter(User.email == self.email).one()

        if not user:
            raise Exception("Usuário e/ou senha inválidos")

        if not self._check_password_hash(user.password):
            raise Exception("Usuário e/ou senha inválidos")
        return user

    @classmethod
    def to_encrypt(self, password):
        return generate_password_hash(password.encode())

    def _check_password_hash(self, password):
        return check_password_hash(password, self.password)

    def update_last_login(self):
        self.last_login = db.func.current_timestamp()
        db.session.merge(self)
        db.session.commit()

    @classmethod
    def find_by_token(cls, token):
        token = bytes(token, "ascii")
        return db.session.query(User).filter(User.token == token).one()

    def is_valid_login(self):
        if ((datetime.now() - self.last_login).total_seconds() / 60.0) > 30:
            raise ExceptionCloseTime("Tempo encerrado.")


@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, instance):
    instance.password = instance.to_encrypt(instance.password)
    instance.token = jwt_encode(instance.email)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(9))
    ddd = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
