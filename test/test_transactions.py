def test_add_transaction(client):
    response = client.post("/transactions/add",json={
        "type":"income",
        "amount":100,
        "category":"Salary",
        "description": "Monthly Salary"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
