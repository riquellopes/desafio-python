# import datetime
import os
import jwt
from app.db import db


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

    def __init__(self, *args, **kwargs):
        kwargs.update({
            "token": jwt.encode({"email": kwargs["email"]}, os.environ.get("DESAFIO_SECRET_KEY"), algorithm='HS256')
        })
        super(User, self).__init__(*args, **kwargs)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(9))
    ddd = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
