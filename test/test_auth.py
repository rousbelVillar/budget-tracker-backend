def test_register_and_login(client):
    res = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass'
    })
    assert res.status_code == 201

    res = client.post('/login', json={
        'username': 'testuser',
        'password': 'securepass'
    })
    assert res.status_code == 200
    assert b'Login successful' in res.data
