from fastapi import APIRouter, status

from pkm_sim_api.schemas.competitive_pokemon_schema import CompetitivePokemonSchema
from pkm_sim_api.services.competitive_pokemon_service import CompetitivePokemonService

router = APIRouter(prefix='/competitive', tags=['competitive'])
comp_pkm_serv = CompetitivePokemonService()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_competitive_pokemon(body: CompetitivePokemonSchema) -> None:
    await comp_pkm_serv.create_competitive_pokemon(body.model_dump())