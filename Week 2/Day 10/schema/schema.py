from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The name of the inventory item",
    )
    price: float = Field(
        ...,
        description="Price of the inventory item",
    )
    quantity: int = Field(
        ...,
        description="Quantity of the inventory item",
    )


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
