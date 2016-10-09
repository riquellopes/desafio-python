from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import ModelSchema

from app.models import User
from app.db import db


class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

    @validates("email")
    def validate_email(self, value):
        count = self.session.query(self.Meta.model).filter(self.Meta.model.email == value).count()

        if count:
            raise ValidationError("E-mail já existente")


class UserLoginRequestSchema(ModelSchema):

    class Meta:
        model = User
        sqla_session = db.session
