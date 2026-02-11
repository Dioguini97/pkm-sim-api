from fastapi import APIRouter

from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.services.move_service import MoveService

router = APIRouter(prefix='/move', tags=['move'])
move_service = MoveService()

@router.get('/{name}')
async def get_move(name: str):
    try:
        move = await move_service.get_move(name)
        if not move:
            raise PokemonSimAPIException(message=f'Não foi possível devolver move: {name}', status_code=500)
        else:
            return move
    except Exception as e:
        raise PokemonSimAPIException(message=f'Erro: {e}', status_code=500, error_code=ErrorCode.POKE_SIM_GENERAL_ERROR)