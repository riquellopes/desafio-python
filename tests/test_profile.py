# from datetime import datetime, timedelta
import json
from .factories import UserFactory
from app.decorators import User
from app.exceptions import ExceptionCloseTime


def test_when_to_sended_a_empty_token_service_respose_401(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    response = test_client.get("/profile")
    assert response.status_code == 401


def test_when_to_sended_a_invalid_token_service_respose_401(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    response = test_client.get("/profile", headers={"X-TOKEN": 'XXXXXXXX'})
    assert response.status_code == 401


def test_should_be_returned_status_403_for_time_closed(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    is_valid_login = mocker.patch.object(User, "is_valid_login")
    is_valid_login.side_effect = ExceptionCloseTime("Tempo encerrado")

    # datetime.now() + timedelta(hours=9)

    user = UserFactory(email="time@end.com")

    response = test_client.get(
        "/profile", headers={"X-TOKEN": user.token})

    assert response.status_code == 403

    data = json.loads(response.data.decode('utf-8'))
    assert data['mensagem'] == "Sessão inválida"


def test_when_header_x_token_is_valid_status_code_200(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    user = UserFactory(email="ll@ll.com")
    assert user.token is not None

    response = test_client.get(
        "/profile", headers={"X-TOKEN": user.token})

    assert response.status_code == 200
