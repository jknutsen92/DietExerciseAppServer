from fastapi            import Depends
from argon2             import PasswordHasher
from fastapi.security   import OAuth2PasswordBearer, APIKeyHeader
from pydantic           import BaseModel, EmailStr
from json               import load
from dbs                import db, User

ADMIN_KEYS = "./keys/admin.json"
with open(ADMIN_KEYS) as file:
    admins = load(file)

class AuthAdmin(BaseModel):
    user:       EmailStr
    key:        str

class AuthUser(BaseModel):
    id:         int
    email:      EmailStr
    first_name: str
    last_name:  str

oauth2_scheme_user =    OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_admin =   APIKeyHeader(name="admin_key")

async def get_current_user(token: str = Depends(oauth2_scheme_user)):
    user = await db.fetch_one(User.select().where(User.c.id == int(token)))
    return AuthUser(id=int(token), email=user["email"], first_name=user["first_name"], last_name=user["last_name"])

async def get_current_admin(token: str = Depends(oauth2_scheme_admin)):
    return token

ph = PasswordHasher()