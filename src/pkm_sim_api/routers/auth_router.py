from fastapi import APIRouter

from pkm_sim_api.configs.auth_handler import create_access_token
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.repositories.user_repository import UserRepository

router = APIRouter(prefix='/auth')
user_repository = UserRepository()

@router.post('/login')
async def login(payload: dict):
    username = payload.get('username')
    psw = payload.get('password')

    user = await user_repository.find_by_username(username)

    if user['psw'] == psw:
        token = create_access_token(
            data={
                'sub': username,
                'role': user['role']
            }
        )
        return {
            'access_token': token,
            'token_type': 'bearer'
        }
    raise PokemonSimAPIException(message=f'Password incorreta para username {username}', status_code=401, error_code=ErrorCode.USER_ERROR)

@router.put('/signin')
async def signin(payload: dict):
    username = payload.get('username')
    user = await user_repository.find_by_username(username)
    if user:
        raise PokemonSimAPIException(message='Username already at use')
    else:
        await user_repository.create(payload)
        return login(payload)