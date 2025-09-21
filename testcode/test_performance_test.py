

from fastapi.testclient import TestClient
from sourcecode.performance_test import api

client = TestClient(api)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}

def test_add_book():
    book = {
        "id": 1,
        "name": "Test Book",
        "description": "A test book",
        "isAvailable": True
    }
    response = client.post("/book", json=book)
    assert response.status_code == 200
    assert any(b["id"] == 1 for b in response.json())

def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_book():
    updated_book = {
        "id": 1,
        "name": "Updated Book",
        "description": "Updated description",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_book)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Book"

def test_update_book_not_found():
    updated_book = {
        "id": 999,
        "name": "Nonexistent Book",
        "description": "Should not exist",
        "isAvailable": False
    }
    response = client.put("/book/999", json=updated_book)
    assert response.status_code == 200
    assert response.json()["error"] == "Book Not Found"

def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_book_not_found():
    response = client.delete("/book/999")
    assert response.status_code == 200
    assert response.json()["error"] == "Book not found, deletion failed"