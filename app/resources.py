import http
from flask import make_response, jsonify
from flask_restful import Resource
from webargs.flaskparser import use_args
from app.schemas import UserSchema, UserLoginRequestSchema
from app.db import db


def default_return(user):
    return UserSchema(only=("id", "created", "modified", "last_login", "token")).dumps(user).data


class UserCreateResource(Resource):

    @use_args(UserSchema(strict=True))
    # @TODO o padrão de saida de mensagem é {"menssage": "descrição do erro"}
    def post(self, args):
        user = args

        db.session.add(user)
        db.session.commit()

        return make_response(default_return(user), http.HTTPStatus.CREATED)


class UserLoginResource(Resource):

    @use_args(UserLoginRequestSchema(strict=True))
    def post(self, args):
        try:
            user = args.to_authorize()
            user.update_last_login()
            return make_response(default_return(user), http.HTTPStatus.ACCEPTED)
        except:
            return make_response(
                jsonify(dict(mensagem="Usuário e/ou senha inválidos")), 401)
