import json


def test_should_be_returned_a_valid_dict(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    data = {
        "name": "João da Silva",
        "email": "joao@silva.org",
        "password": "hunter2",
        "phones": [{"number": "987654321", "ddd": "21"}]
    }
    response = test_client.post("/user", data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201

    data = json.loads(response.data.decode('utf-8'))

    assert "id" in data
    assert "created" in data
    assert "modified" in data
    assert "last_login" in data
    assert "token" in data


def test_should_be_returned_error_message(test_client, mocker):
    os = mocker.patch("app.models.os")
    os.environ.get.return_value = "desafio_python"

    data = {
        "name": "João da Silva",
        "email": "joao@silva.org",
        "password": "hunter2",
        "phones": [{"number": "987654321", "ddd": "21"}]
    }
    response = test_client.post("/user", data=json.dumps(data), content_type='application/json')

    assert response.status_code == 422

    data = json.loads(response.data.decode('utf-8'))
    assert data['messages']['email'][0] == "E-mail já existente"
