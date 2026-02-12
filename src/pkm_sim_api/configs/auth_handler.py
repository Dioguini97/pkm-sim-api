from fastapi.security import HTTPBearer

security = HTTPBearer()

def create_access_token(data: dict):
