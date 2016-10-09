import http
from sqlalchemy.orm.exc import NoResultFound
from flask import request, make_response, jsonify
from functools import wraps

from app.models import User
from app.exceptions import ExceptionCloseTime


def build_response(message, status):
    return make_response(jsonify({
        "mensagem": message}
    ), status)


def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
            - Caso o token não exista, retornar erro com status apropriado com a mensagem "Não autorizado". OK
            - Caso o token exista, buscar o usuário pelo id passado no path e comparar se o token no modelo
              é igual ao token passado no header. OK
            - Caso não seja o mesmo token, retornar erro com status apropriado e mensagem "Não autorizado" OK
            - Caso seja o mesmo token, verificar se o último login foi a MENOS que 30 minutos atrás.
            - Caso não seja a MENOS que 30 minutos atrás, retornar erro com status apropriado com mensagem
              "Sessão inválida".
            - Caso tudo esteja ok, retornar o usuário no mesmo formato do retorno do Login.
        """

        token = request.headers.get("X-TOKEN", None)
        if not token:
            return build_response("Não autorizado", http.HTTPStatus.UNAUTHORIZED)

        try:
            user = User.find_by_token(token)
            user.is_valid_login()

            kwargs.update({
                "user": user
            })
            func(*args, **kwargs)
        except NoResultFound:
            return build_response("Não autorizado", http.HTTPStatus.UNAUTHORIZED)
        except ExceptionCloseTime:
            return build_response("Sessão inválida", http.HTTPStatus.FORBIDDEN)
    return wrapper
