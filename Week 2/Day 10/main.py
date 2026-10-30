from fastapi import FastAPI, HTTPException, status
from typing import List
from schema.schema import ItemCreate, ItemUpdate
from services.service import inventory_service

app = FastAPI()

@app.get("/items", response_model=List[dict])
def read_all_items():
    return inventory_service.get_all()

@app.get("/items/{item_id}", response_model=dict)
def read_item_by_id(item_id: int):
    item = inventory_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate):
    return inventory_service.create(item_in)

@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: int, item_in: ItemUpdate):
    updated_item = inventory_service.update(item_id, item_in)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    success = inventory_service.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
