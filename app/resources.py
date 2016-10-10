import http
from flask import make_response, jsonify
from flask_restful import Resource
from webargs.flaskparser import FlaskParser, abort
from app.schemas import UserSchema, UserLoginRequestSchema
from app.db import db
from app.decorators import token_required


def default_return(user):
    return UserSchema(only=("id", "created", "modified", "last_login", "token")).dumps(user).data


class MPaser(FlaskParser):
    default_error_messages = {
        'Missing data for required field.': 'Algumas informações não foram preenchidas.',
        'Invalid input type.': 'Tipo invalida.',
        'Field may not be null.': 'Campo não pode ser nulo.',
        'Invalid value.': 'Valor invalido.'
    }

    def translate(self, message):
        try:
            message = self.default_error_messages[message]
        except KeyError:
            pass
        return message

    def handle_error(self, error):
        errors = set()
        for erro in error.messages.items():
            message = self.translate("".join(erro[1]))
            errors.add(message)
        status_code = getattr(error, 'status_code', self.DEFAULT_VALIDATION_STATUS)
        messages = " ".join(errors)
        abort(status_code, mensagem=messages, exc=error)


use_args = MPaser().use_args


class UserCreateResource(Resource):

    @use_args(UserSchema(strict=True), locations=("json", ))
    def post(self, args):
        user = args

        db.session.add(user)
        db.session.commit()

        return make_response(default_return(user), http.HTTPStatus.CREATED)


class UserLoginResource(Resource):

    @use_args(UserLoginRequestSchema(strict=True, only=("email", "password", )), locations=("json", ))
    def post(self, args):
        try:
            user = args.to_authorize()
            user.update_last_login()
            return make_response(default_return(user), http.HTTPStatus.ACCEPTED)
        except:
            return make_response(
                jsonify(dict(mensagem="Usuário e/ou senha inválidos")), 401)


class UserProfileResource(Resource):

    @token_required
    def get(self, user):
        return make_response(default_return(user), http.HTTPStatus.OK)
