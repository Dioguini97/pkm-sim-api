from pkm_sim_commons import Pokemon, CompetitivePokemon

from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.repositories import CompetitivePokemonRepository


class CompetitivePokemonService:
    def __init__(self):
        self.repository = CompetitivePokemonRepository()

    async def create_competitive_pokemon(self, payload: dict) -> None:

        pkm = Pokemon(**payload['pkm'])
        competitive = CompetitivePokemon(
            user=payload["user"],
            name=payload["name"],
            nickname=payload.get("nickname"),
            ability=payload["ability"],
            nature=payload["nature"],
            moves=payload["moves"],
            pkm=pkm,
            ivs=payload.get("ivs"),
            evs=payload.get("evs"),
            item=payload.get("item"),
            level=payload.get("level", 50)
        )

        data_to_store = payload.copy()
        data_to_store['raw_stats'] = competitive.raw_stats

        try:
            return await self.repository.create(data_to_store)
        except Exception as e:
            raise PokemonSimAPIException(
                status_code=500, message=e.__str__(), error_code=ErrorCode.DATA_BASE_ERROR
            )