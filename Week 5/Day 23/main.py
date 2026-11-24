"""
Day 23 - Shared Services Across REST & GraphQL
Demonstrates unified business rules between REST endpoints and Ariadne GraphQL mutations.
Enforces title validation (5-80 chars), status transitions, and resource ownership.
"""

import os
from typing import Optional
from fastapi import FastAPI, Request, Header, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from services.item_service import ItemService
from domain.exceptions import (
    DomainValidationError,
    DomainPermissionError,
    DomainNotFoundError
)
from graphql_api.resolvers import bindables

app = FastAPI(
    title="Day 23: Shared Services (REST & GraphQL Parity)",
    description="Unified business rules across REST endpoints and GraphQL mutations."
)

# --- Global Exception Handlers for REST Transport ---
@app.exception_handler(DomainValidationError)
async def validation_exc_handler(request: Request, exc: DomainValidationError):
    """Maps domain validation failures to HTTP 400 Bad Request."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": "VALIDATION_ERROR", "detail": str(exc)}
    )

@app.exception_handler(DomainPermissionError)
async def permission_exc_handler(request: Request, exc: DomainPermissionError):
    """Maps domain permission failures to HTTP 403 Forbidden."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"code": "FORBIDDEN", "detail": str(exc)}
    )

@app.exception_handler(DomainNotFoundError)
async def not_found_exc_handler(request: Request, exc: DomainNotFoundError):
    """Maps domain not-found failures to HTTP 404 Not Found."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": "NOT_FOUND", "detail": str(exc)}
    )


# --- Pydantic Schemas for REST Layer ---
class CreateItemSchema(BaseModel):
    title: str = Field(..., description="Task title (5-80 chars)")
    state: str = Field(default="OPEN", description="Initial status: OPEN, IN_PROGRESS, DONE")


class UpdateItemSchema(BaseModel):
    title: Optional[str] = Field(default=None, description="Updated task title")
    state: Optional[str] = Field(default=None, description="Target state")


# --- REST Endpoints ---
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "day": 23}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item_rest(payload: CreateItemSchema, x_user_id: str = Header("user_123")):
    """Creates item through shared ItemService."""
    return ItemService.create_item(payload.title, payload.state, x_user_id)

@app.get("/items/{item_id}")
def get_item_rest(item_id: str, x_user_id: str = Header("user_123")):
    """Retrieves item through shared ItemService."""
    return ItemService.get_item(item_id, x_user_id)

@app.patch("/items/{item_id}")
def update_item_rest(item_id: str, payload: UpdateItemSchema, x_user_id: str = Header("user_123")):
    """Updates item through shared ItemService."""
    return ItemService.update_item(item_id, payload.title, payload.state, x_user_id)

@app.delete("/items/{item_id}")
def delete_item_rest(item_id: str, x_user_id: str = Header("user_123")):
    """Deletes item through shared ItemService."""
    return ItemService.delete_item(item_id, x_user_id)


# --- Mount Ariadne GraphQL ---
schema_file = os.path.join(os.path.dirname(__file__), "graphql_api", "schema.graphql")
type_defs = load_schema_from_path(schema_file)
schema = make_executable_schema(type_defs, *bindables)

def get_context_value(request: Request):
    """Provides verified user identity in GraphQL resolver context."""
    user_id = request.headers.get("x-user-id", "user_123")
    return {"request": request, "user_id": user_id}

# Mount at /graphql
app.mount("/graphql", GraphQL(schema, context_value=get_context_value, debug=True))
