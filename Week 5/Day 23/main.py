# main.py
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from services.item_service import ItemService
from domain.exceptions import (
    DomainValidationError,
    DomainPermissionError,
    DomainNotFoundError
)
from graphql_api.resolvers import mutation

app = FastAPI()

# --- Global Exception Handlers for REST ---
@app.exception_handler(DomainValidationError)
async def validation_exc_handler(request: Request, exc: DomainValidationError):
    return JSONResponse(status_code=400, content={"code": "VALIDATION_ERROR", "detail": str(exc)})

@app.exception_handler(DomainPermissionError)
async def permission_exc_handler(request: Request, exc: DomainPermissionError):
    return JSONResponse(status_code=403, content={"code": "FORBIDDEN", "detail": str(exc)})

@app.exception_handler(DomainNotFoundError)
async def not_found_exc_handler(request: Request, exc: DomainNotFoundError):
    return JSONResponse(status_code=404, content={"code": "NOT_FOUND", "detail": str(exc)})

# --- Pydantic Schemas (Structural typing only, no business rules) ---
class CreateItemSchema(BaseModel):
    title: str
    state: str

class UpdateItemSchema(BaseModel):
    title: Optional[str] = None
    state: Optional[str] = None

# --- REST Routes ---
@app.post("/items", status_code=201)
def create_item_rest(payload: CreateItemSchema, x_user_id: str = Header("user_123")):
    return ItemService.create_item(payload.title, payload.state, x_user_id)

@app.patch("/items/{item_id}")
def update_item_rest(item_id: str, payload: UpdateItemSchema, x_user_id: str = Header("user_123")):
    return ItemService.update_item(item_id, payload.title, payload.state, x_user_id)

@app.delete("/items/{item_id}")
def delete_item_rest(item_id: str, x_user_id: str = Header("user_123")):
    return ItemService.delete_item(item_id, x_user_id)

# --- Mount Ariadne GraphQL ---
type_defs = load_schema_from_path("graphql_api/schema.graphql")
schema = make_executable_schema(type_defs, mutation)

def get_context_value(request):
    return {"request": request, "user_id": request.headers.get("x-user-id", "user_123")}

app.mount("/graphql", GraphQL(schema, context_value=get_context_value, debug=True))
