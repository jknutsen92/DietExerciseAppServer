from fastapi            import Depends, HTTPException
from typing             import Optional
from datetime           import timedelta, datetime
from argon2             import PasswordHasher
from fastapi.security   import OAuth2PasswordBearer, APIKeyHeader
from pydantic           import BaseModel, EmailStr
from dbs                import db, User
from jose               import jwt, JWTError
from hashlib            import sha1

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES =   60
ALGORITHM =                     "HS256"
SECRET_KEY =                    "a3563bd450da56146ab162ad7e38bc8036f6ca37755284a5fad86331adf1eea4"

admins = {
    "ceb1bb68e0ac9c877e561596b1cc5bf4aae1722c": "jknutsen92@gmail.com"
}

class AuthUser(BaseModel):
    id:         str
    email:      EmailStr
    first_name: str
    last_name:  str
    is_admin:   bool

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme_user)):
    unauthorized = HTTPException(
        status_code=401,
        detail="Could not validate token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    try:
        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        id = data.get("sub")
        if not id:
            raise unauthorized
    except JWTError as e:
        print(e)
        raise unauthorized

    user = await db.fetch_one(User.select().where(User.c.id == id))
    return AuthUser(
        id=id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_admin=id in admins
    )

def create_access_token(data: dict, expires: Optional[timedelta] = None):
    data = data.copy()
    if expires:
        expiration = datetime.utcnow() + expires
    else:
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update(
        {
            "exp": expiration
        }
    )
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def sha1_hash(string: str):
    sha = sha1()
    sha.update(string.encode("utf-8"))
    return sha.hexdigest()

ph = PasswordHasher()