from fastapi import APIRouter

from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.services.item_service import ItemService

router = APIRouter(prefix='/item', tags=['move'])
item_service = ItemService()

@router.get('/{name}')
async def get_item(name: str):
    try:
        item = await item_service.get_item(name)
        if not item:
            raise PokemonSimAPIException(message='General Error', error_code=ErrorCode.POKE_SIM_GENERAL_ERROR, status_code=500)
        return item
    except Exception as e:
        raise PokemonSimAPIException(message='General Error', error_code=ErrorCode.POKE_SIM_GENERAL_ERROR, status_code=500)