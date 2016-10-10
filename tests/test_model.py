import pytest
from datetime import datetime, timedelta
from app.db import db
from app.models import User
from app.exceptions import ExceptionCloseTime


def test_method_return_true_when_last_login_is_before_30_minutes():
    user = User(**{
        "name": "Henrique Lopes",
        "password": "111111",
        "email": "riquellopes@g.com",
        "last_login": datetime.now()
    })

    assert user.is_valid_login()


def test_method_raise_exception_when_last_login_is_after_30_minutes():
    user = User(**{
        "name": "Henrique Lopes",
        "password": "111111",
        "email": "riquellopes@g.com",
        "last_login": datetime.now() + timedelta(hours=9)
    })

    with pytest.raises(ExceptionCloseTime) as e:
        user.is_valid_login()
    assert "Tempo encerrado." in str(e.value)


def test_validation_process_auth(mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"
    user = User(**{
        "name": "Henrique Lopes",
        "password": "111111",
        "email": "riquellopes@g.com"
    })

    db.session.add(user)
    db.session.commit()

    assert user.to_authorize().id == user.id

    user = User(**{
        "name": "Henrique Lopes",
        "password": "123456",
        "email": "riquellopes@g.com"
    })

    with pytest.raises(Exception) as e:
        user.to_authorize()
    assert "Usuário e/ou senha inválidos" in str(e.value)
