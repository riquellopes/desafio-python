import http
from flask import make_response, jsonify
from flask_restful import Resource
from webargs.flaskparser import use_args
from app.schemas import UserPostSchema, UserSchema, user_schema
from app.db import db


class UserCreateResource(Resource):

    @use_args(UserPostSchema(strict=True))
    def post(self, args):
        user, errors = user_schema.load(args)

        if errors:
            # @TODO o padrão de saida de mensagem é {"menssage": "descrição do erro"}
            return make_response(jsonify(errors), http.HTTPStatus.PRECONDITION_FAILED)

        db.session.add(user)
        db.session.commit()

        data = UserSchema(only=("id", "created", "modified", "last_login", "token")).dumps(user).data
        return make_response(data, http.HTTPStatus.CREATED)


class UserLoginResource(Resource):
    pass
