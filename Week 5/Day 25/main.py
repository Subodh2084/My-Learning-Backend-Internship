"""
Day 25 FastAPI & Ariadne Application
Exposes the Ariadne GraphQL endpoint at /graphql and a REST health check.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from database import engine, SessionLocal, init_db
from models import User
from resolvers import bindables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Bootstraps database on application startup."""
    init_db()
    yield


app = FastAPI(
    title="TaskFlow GraphQL Service (Day 25 Review)",
    description="Full implementation of the Shared GraphQL Contract with Ariadne.",
    lifespan=lifespan
)

# Load schema definition
schema_path = os.path.join(os.path.dirname(__file__), "schema.graphql")
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, *bindables)


async def get_graphql_context(request: Request) -> dict:
    """Builds context containing database session and authenticated user."""
    db = SessionLocal()
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if "Bearer " in auth_header else ""

    user = db.query(User).filter(User.token == token).first() if token else None

    return {
        "request": request,
        "db": db,
        "user": user,
    }


# Mount Ariadne ASGI server
graphql_app = GraphQL(schema, context_value=get_graphql_context, debug=True)
app.mount("/graphql", graphql_app)


@app.get("/health")
def health():
    return {"status": "ok", "day": 25, "service": "taskflow-graphql"}
