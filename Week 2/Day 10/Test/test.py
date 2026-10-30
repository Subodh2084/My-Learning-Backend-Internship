import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from main import app
client=TestClient(app)
class ItemSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    price: float = Field(...)


ITEMS_DB = {
    1: {"id": 1, "name": "Mechanical Keyboard", "price": 99}
}






def test_get_item_valid():
    response = client.get("/items/1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 99


def test_get_item_invalid_not_found():
    response = client.get("/items/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    assert response.json() == {"detail": "Item not found"}


def test_create_item_valid():
    new_item = {"id": 2, "name": "Wireless Mouse", "price": 49.50,"quantity":5}
    response = client.post("/items/", json=new_item)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "Wireless Mouse"





def test_create_item_invalid_schema():
    bad_schema_item = {"id": 3, "name": "X","quantity":5}  # Short name, negative price
    response = client.post("/items/", json=bad_schema_item)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    errors = response.json()["detail"]
    error_locations = [err["loc"][-1] for err in errors]
    assert "name" in error_locations
    



@pytest.mark.xfail(reason="Deliberately wrong expectation to satisfy acceptance criteria")
def test_deliberate_failure_check():
    response = client.get("/items/1")
    
    
    assert response.json()["name"] == "Completely Wrong Expected Name"
