"""
Day 24 - Ariadne GraphQL API with Bounded Pagination and N+1 Monitoring
Mounts Ariadne on FastAPI and provides request-scoped context including DB session and verified user.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session

from database import engine, SessionLocal, init_db
from models import User
from resolvers import bindables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes in-memory database and synthetic seed data on startup."""
    init_db()
    yield


app = FastAPI(
    title="Day 24: Bounded GraphQL Pagination & Query Investigation",
    lifespan=lifespan
)

# Load schema
schema_path = os.path.join(os.path.dirname(__file__), "schema.graphql")
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, *bindables)


def get_db():
    """Request-scoped database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_graphql_context(request: Request) -> dict:
    """Builds GraphQL context with verified user and database session."""
    db = SessionLocal()
    # Mock token extraction for educational lab (production uses verified JWT)
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if "Bearer " in auth_header else "alice-secret-token"

    user = db.query(User).filter(User.token == token).first()

    return {
        "request": request,
        "db": db,
        "user": user,
    }


# Mount Ariadne ASGI endpoint
graphql_app = GraphQL(schema, context_value=get_graphql_context, debug=True)
app.mount("/graphql", graphql_app)


@app.get("/health")
def health():
    return {"status": "ok", "day": 24}
