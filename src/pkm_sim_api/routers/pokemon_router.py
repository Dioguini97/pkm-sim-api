from fastapi import APIRouter
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException
from ..services.pokemon_service import PokemonService

router = APIRouter(prefix='/pokemon', tags=['pokemon'])
pokemon_service = PokemonService()

@router.get('/{name}')
async def get_pokemon(name: str):
    # cache_key = f"pokemon:{name}"
    #
    # if CACHE.redis:
    #     try:
    #         cached = await CACHE.redis.get(cache_key)
    #         if cached:
    #             return json.loads(cached)
    #     except Exception as e:
    #         print(f'Erro ao buscar chache: {e}')

    try:
        pkm = await pokemon_service.get_pokemon(name)
        if not pkm:
            raise PokemonSimAPIException(status_code=404, message=f'Pokemon {name} não encontrado!')

        # if CACHE.redis:
        #     try:
        #         await CACHE.redis.setex(
        #             cache_key, 3600, json.dumps(pkm)
        #         )
        #
        #     except Exception as e:
        #         print(f'Erro ao salvar na cache: {e}')

        return pkm
    except PokemonSimAPIException as e:
        raise PokemonSimAPIException(status_code=500, message=str(e))

