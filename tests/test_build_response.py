import json
from app.decorators import build_response


def test_when_a_status_code_isnt_defined_the_default_is_200(test_client):

    with test_client.application.test_request_context():
        response = build_response("Fala Jovem")

        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data['mensagem'] == "Fala Jovem"
        assert response.headers.get("Content-Type") == "application/json"
