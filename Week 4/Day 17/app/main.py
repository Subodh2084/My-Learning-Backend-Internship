from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pwdlib import PasswordHash
from app.models import TokenOut, UserInDB, UserLoginInput, UserPublic, UserRegisterInput

SECRET_KEY = "replace-with-a-strong-env-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
hasher = PasswordHash.recommended()  # Argon2
bearer = HTTPBearer(auto_error=False)

users_db: dict[str, UserInDB] = {}
records_db: dict[str, str] = {}


def create_access_token(user_id: str, email: str) -> str:
  now = datetime.now(timezone.utc)
  payload = {
      "sub": user_id,
      "email": email,
      "iat": now,
      "exp": now + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
  }
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> UserInDB:
  if not creds:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials"
    )
  try:
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("email")
    user = users_db.get(email) if email else None
    if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
      )
    return user
  except jwt.ExpiredSignatureError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
    )
  except jwt.InvalidTokenError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )


@app.post(
    "/auth/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserRegisterInput):
  data.email=data.email.strip().lower()
  data.username=data.username.strip().lower()
  if data.email in users_db:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
    )

  user_id = f"user_{len(users_db) + 1}"
  record = UserInDB(
      id=user_id,
      email=data.email,
      username=data.username,
      password_hash=hasher.hash(data.password),
      created_at=datetime.now(timezone.utc),
  )
  users_db[data.email] = record
  records_db[user_id] = f"Private data owned by {data.username}"
  return record


@app.post("/auth/login", response_model=TokenOut)
def login(data: UserLoginInput):
  user = users_db.get(data.email)
  if not user or not hasher.verify(data.password, user.password_hash):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )
  token = create_access_token(user.id, user.email)
  return TokenOut(access_token=token, expires_in=TOKEN_EXPIRE_MINUTES * 60)


@app.get("/auth/me", response_model=UserPublic)
def me(current_user: UserInDB = Depends(get_current_user)):
  return current_user


@app.get("/records/{owner_id}")
def read_record(owner_id: str, current_user: UserInDB = Depends(get_current_user)):
  if current_user.id != owner_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not record owner"
    )
  return {"owner_id": owner_id, "secret": records_db[owner_id]}

