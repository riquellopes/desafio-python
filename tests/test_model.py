import pytest
from datetime import datetime, timedelta
from app.models import User
from app.exceptions import ExceptionCloseTime


def test_method_returno_true_when_last_login_before_30_minutes():
    user = User(**{
        "name": "Henrique Lopes",
        "password": "111111",
        "email": "riquellopes@g.com",
        "last_login": datetime.now()
    })

    assert user.is_valid_login()


def test_method_returno_true_when_last_login_after_30_minutes():
    user = User(**{
        "name": "Henrique Lopes",
        "password": "111111",
        "email": "riquellopes@g.com",
        "last_login": datetime.now() + timedelta(hours=9)
    })

    with pytest.raises(ExceptionCloseTime) as e:
        user.is_valid_login()
    assert "Tempo encerrado." in str(e.value)
