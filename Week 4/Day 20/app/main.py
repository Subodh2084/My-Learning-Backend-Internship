import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash

# 1. Configuration & Secrets (Injected via environment variables)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-do-not-use-in-prod-32bytes!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
IS_PROD = os.environ.get("ENV") == "production"

# 2. Safe Logging Setup (Redact sensitive fields in production log formatters)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("security_audit")

app = FastAPI(title="Secure FastAPI Service")

# 3. Strict CORS Whitelist
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Never use ["*"] with allow_credentials=True
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# 4. Safe Global Exception Handler (Prevents stack trace leaks)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {type(exc).__name__}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

# --- Mock Database & Password Hasher ---
password_hasher = PasswordHash.recommended()
FAKE_USERS_DB = {}
FAKE_NOTES_DB = {
    1: {"id": 1, "owner_email": "alice@example.com", "content": "Alice's secret note"},
    2: {"id": 2, "owner_email": "bob@example.com", "content": "Bob's secret note"},
}

class AuthPayload(BaseModel):
    email: EmailStr
    password: str

# --- Auth Helpers ---
def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in FAKE_USERS_DB:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")

# --- Routes ---
@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(payload: AuthPayload):
    if payload.email in FAKE_USERS_DB:
        # Generic message to prevent user enumeration
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")
    
    FAKE_USERS_DB[payload.email] = {
        "email": payload.email,
        "hashed_password": password_hasher.hash(payload.password),
    }
    logger.info(f"User registered: {payload.email}")
    return {"message": "Account created"}

@app.post("/auth/login")
async def login(payload: AuthPayload, response: Response):
    user = FAKE_USERS_DB.get(payload.email)
    # Always verify against a dummy hash if user doesn't exist to prevent timing attacks
    dummy_hash = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG"
    target_hash = user["hashed_password"] if user else dummy_hash

    if not password_hasher.verify(payload.password, target_hash) or not user:
        logger.warning(f"Failed login attempt for: {payload.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user["email"])
    
    # Set Hardened HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,                # Blocks JS document.cookie access (XSS protection)
        secure=IS_PROD,               # Enforces HTTPS in production
        samesite="strict",            # Mitigates CSRF
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    logger.info(f"User logged in: {user['email']}")
    return {"message": "Authenticated"}

@app.get("/notes/{note_id}")
async def read_private_note(
    note_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
):
    note = FAKE_NOTES_DB.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    # Ownership Verification Check (Prevents IDOR / Horizontal Privilege Escalation)
    if note["owner_email"] != current_user:
        logger.warning(f"Unauthorized access attempt by {current_user} on note {note_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        
    return note
