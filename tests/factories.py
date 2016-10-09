from factory import RelatedFactory, lazy_attribute
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.models import User, Phone, jwt_encode
from app.db import db


class PhoneFactory(Factory):
    class Meta:
        model = Phone
        sqlalchemy_session = db.session

    number = "987654321"
    ddd = "21"


class UserFactory(Factory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    name = "Henrique Lopes"
    email = "henrique@lopes.org"
    password = User.to_encrypt("lopes2")
    phones = RelatedFactory(PhoneFactory, 'user')

    @lazy_attribute
    def token(self):
        return jwt_encode(self.email)
