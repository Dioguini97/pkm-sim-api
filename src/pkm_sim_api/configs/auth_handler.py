import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security
from datetime import datetime, timedelta, timezone

from .config import settings
from .pkm_sim_api_exception import PokemonSimAPIException, ErrorCode

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(
            auth.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise PokemonSimAPIException(status_code=401, message='Token expired!', error_code=ErrorCode.TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        raise PokemonSimAPIException(status_code=401, message='Invalid Token', error_code=ErrorCode.TOKEN_INVALID)