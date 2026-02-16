from fastapi import APIRouter

from pkm_sim_api.services.ability_service import AbilityService

router = APIRouter(prefix='/ability', tags=['ability'])
service = AbilityService()

@router.get('/{name}')
async def get_ability(name: str):
    return await service.get_ability(name)