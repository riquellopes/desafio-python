import json
from .factories import UserFactory


def test_should_be_returned_status_401_when_not_a_json_application(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"
    user = UserFactory.create()

    data = {
        "email": user.email,
        "password": user.password
    }

    response = test_client.post("/login", data=json.dumps(data))

    assert response.status_code == 401


def test_should_be_returned_status_202(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"
    user = UserFactory.create()

    data = {
        "email": user.email,
        "password": user.password
    }

    response = test_client.post("/login", data=json.dumps(data), content_type='application/json')

    assert response.status_code == 202


def test_should_be_returned_status_401(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    data = {
        "email": "jonas",
        "password": "block"
    }

    response = test_client.post("/login", data=json.dumps(data), content_type='application/json')

    assert response.status_code == 401

    data = json.loads(response.data.decode('utf-8'))

    assert data['mensagem'] == "Usuário e/ou senha inválidos"
