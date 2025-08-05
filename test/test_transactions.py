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
def test_get_transaction(client):
    client.post("/transactions/add",json={
        "type":"income",
        "amount":100,
        "category":"Salary",
        "description": "Monthly Salary"
    })
    response = client.get("/transactions/")
    assert response.status_code == 201 or response.status_code == 200


