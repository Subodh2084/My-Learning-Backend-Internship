from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Input Schemas ---
class UserRegisterInput(BaseModel):
  email: EmailStr
  username: str = Field(min_length=3, max_length=32)
  password: str = Field(min_length=8)


class UserLoginInput(BaseModel):
  email: EmailStr
  password: str = Field(min_length=1)


# --- Internal Record (Never returned to clients) ---
class UserInDB(BaseModel):
  id: str
  email: EmailStr
  username: str
  password_hash: str
  created_at: datetime


# --- Safe Public Schema (Acceptance Check: omits password & password_hash) ---
class UserPublic(BaseModel):
  model_config = ConfigDict(extra="ignore")

  id: str
  email: EmailStr
  username: str
  created_at: datetime


class TokenOut(BaseModel):
  access_token: str
  token_type: str = "bearer"
  expires_in: int = 1800
