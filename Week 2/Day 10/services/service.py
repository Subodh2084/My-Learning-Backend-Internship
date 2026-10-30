from typing import List, Dict, Optional
from schema.schema import ItemCreate, ItemUpdate

class InventoryService:
    def __init__(self):
        
        self._db: Dict[int, dict] = {1:{"id":1,"name":"Mechanical Keyboard","price":99
                                        
                                        ,"quantity":"Hello"}}
        self._current_id: int = 2

    def get_all(self) -> List[dict]:
        return list(self._db.values())

    def get_by_id(self, item_id: int) -> Optional[dict]:
        return self._db.get(item_id)

    def create(self, item_in: ItemCreate) -> dict:
        # Convert Pydantic model to dict and assign an ID
        new_item = item_in.model_dump()
        new_item["id"] = self._current_id
        
        self._db[self._current_id] = new_item
        self._current_id += 1
        return new_item

    def update(self, item_id: int, item_in: ItemUpdate) -> Optional[dict]:
        if item_id not in self._db:
            return None
        
        # Update only the fields provided in the update payload
        update_data = item_in.model_dump(exclude_unset=True)
        self._db[item_id].update(update_data)
        return self._db[item_id]

    def delete(self, item_id: int) -> bool:
        if item_id not in self._db:
            return False
        del self._db[item_id]
        return True

# Instantiate the service singleton expected by main.py
inventory_service = InventoryService()
