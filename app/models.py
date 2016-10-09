import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from sqlalchemy import event


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())
    token = db.Column(db.String(200), unique=True)
    phones = db.relationship('Phone', backref="user", lazy='dynamic')

    def to_authorize(self):
        user = db.session.query(User).filter(User.email == self.email).one()

        if not user:
            raise Exception("Usuário e/ou senha inválidos")

        if not self._check_password_hash(user.password):
            raise Exception("Usuário e/ou senha inválidos")
        return user

    def _to_encrypt(self, password):
        return generate_password_hash(password.encode())

    def _check_password_hash(self, password):
        return check_password_hash(password, self.password)

    def update_last_login(self):
        self.last_login = db.func.current_timestamp()
        db.session.merge(self)
        db.session.commit()


@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, instance):
    instance.password = instance._to_encrypt(instance.password)
    instance.token = jwt.encode({"email": instance.email}, os.environ.get("DESAFIO_SECRET_KEY"), algorithm='HS256')


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(9))
    ddd = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
