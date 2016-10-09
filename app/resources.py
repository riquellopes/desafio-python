import http
from flask import make_response, jsonify
from flask_restful import Resource
from webargs.flaskparser import use_args
from app.schemas import (
    UserCreateResquestSchema, UserCreateResponseSchema, UserLoginRequestSchema)
from app.db import db


class UserCreateResource(Resource):

    @use_args(UserCreateResquestSchema(strict=True))
    def post(self, args):
        user, errors = UserCreateResponseSchema().load(args)

        if errors:
            # @TODO o padrão de saida de mensagem é {"menssage": "descrição do erro"}
            return make_response(jsonify(errors), http.HTTPStatus.PRECONDITION_FAILED)

        db.session.add(user)
        db.session.commit()

        data = UserCreateResponseSchema(only=("id", "created", "modified", "last_login", "token")).dumps(user).data
        return make_response(data, http.HTTPStatus.CREATED)


class UserLoginResource(Resource):

    @use_args(UserLoginRequestSchema(strict=True))
    def post(self, args):
        try:
            user = args.to_authorize()
            user.update_last_login()
            data = UserCreateResponseSchema(
                only=("id", "created", "modified", "last_login", "token")).dumps(user).data
            return make_response(data, http.HTTPStatus.ACCEPTED)
        except:
            return make_response(
                jsonify(dict(mensagem="Usuário e/ou senha inválidos")), 401)
