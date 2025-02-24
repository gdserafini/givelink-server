from http import HTTPStatus


def test_root_returns_hello_world_mesage_200(client):
    message = {'message': 'Hello world!'}
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == message
