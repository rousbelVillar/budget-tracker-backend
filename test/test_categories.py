
def test_add_category(client):
    response = client.post('/categories', json={
        'name': 'Test Category',
        'icon': '🧪'
    })
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['name'] == 'Test Category'
    assert data['icon'] == '🧪'

def test_add_duplicate_category(client):
    client.post('/categories', json={'name': 'Health', 'icon': '💊'})
    response = client.post('/categories', json={'name': 'Health', 'icon': '💊'})

    assert response.status_code == 400 or response.status_code == 409

def test_get_categories(client):
    client.post('/categories', json={'name': 'Groceries', 'icon': '🛒'})
    client.post('/categories', json={'name': 'Rent', 'icon': '🏠'})
    
    response = client.get('/categories')
    data = response.get_json()
    
    assert response.status_code == 200
    assert len(data) == 2
    assert any(cat['name'] == 'Groceries' for cat in data)
    assert any(cat['name'] == 'Rent' for cat in data)
