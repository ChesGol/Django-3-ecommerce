def test_version(client):
    assert client.get('/').status_code == 200
