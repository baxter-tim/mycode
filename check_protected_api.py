from protected_api import create_app

app = create_app("test-reader", "test-admin")
reader = {"Authorization": "Bearer test-reader"}
admin = {"Authorization": "Bearer test-admin"}
with app.test_client() as client:
    assert client.get("/notes").status_code == 401
    assert client.post("/notes", headers=reader, json={"title": "Mars"}).status_code == 403
    assert client.post("/notes", headers=admin, json={"title": ""}).status_code == 400
    assert client.post("/notes", headers=admin, data="hello").status_code == 415
    assert client.post("/notes", headers=admin, json={"title": "x" * 2000}).status_code == 413
    assert client.get("/notes", headers=reader).json["notes"] == []
    assert client.post("/notes", headers=admin, json={"title": "Mars"}).status_code == 201
    result = client.get("/notes", headers=reader)
    assert len(result.json["notes"]) == 1
    assert result.headers["Cache-Control"] == "no-store"
print("Authentication, authorization, validation, and state checks passed.")
