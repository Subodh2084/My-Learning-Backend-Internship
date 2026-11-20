from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from Database import SessionLocal, User, Task, get_db

# ----------------------------------------------------
# Startup Seed Data (For immediate testing)
# ----------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "ariadne_dev").first():
            test_user = User(id=42, username="ariadne_dev", token="valid-token-123")
            test_task = Task(id=101, title="Complete Day 22 Ariadne Mount", owner_id=42)
            db.add_all([test_user, test_task])
            db.commit()
    finally:
        db.close()
    yield

# ----------------------------------------------------
# Auth Verification Dependency
# ----------------------------------------------------
def get_current_user_optional(
    request: Request, 
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Verifies Bearer token against the database."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
        
    token = auth_header.split(" ")[1]
    return db.query(User).filter(User.token == token).first()

# ----------------------------------------------------
# GraphQL Schema & Resolvers
# ----------------------------------------------------
type_defs = """
    type User {
        id: ID!
        username: String!
    }

    type Task {
        id: ID!
        title: String!
        ownerId: ID!
    }

    type Query {
        currentUser: User
        ownTask(id: ID!): Task
    }
"""

query = QueryType()

@query.field("currentUser")
def resolve_current_user(obj: Any, info: Any) -> Optional[User]:
    # SQLAlchemy User instance maps directly to GraphQL User fields
    return info.context.get("user")

@query.field("ownTask")
def resolve_own_task(obj: Any, info: Any, id: str) -> Optional[Dict[str, Any]]:
    user: Optional[User] = info.context.get("user")
    db: Session = info.context.get("db")

    if not user:
        return None

    # Enforce ownership: query by both Task ID and authenticated User ID
    task = db.query(Task).filter(
        Task.id == int(id), 
        Task.owner_id == user.id
    ).first()

    if not task:
        return None

    return {
        "id": task.id,
        "title": task.title,
        "ownerId": task.owner_id
    }

schema = make_executable_schema(type_defs, query)

# ----------------------------------------------------
# Context Builder & ASGI Mount
# ----------------------------------------------------
async def get_graphql_context(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
) -> Dict[str, Any]:
    return {
        "request": request,
        "db": db,
        "user": user,
    }

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQL(
    schema,
    context_value=get_graphql_context,
    debug=True
)

app.mount("/graphql", graphql_app)
