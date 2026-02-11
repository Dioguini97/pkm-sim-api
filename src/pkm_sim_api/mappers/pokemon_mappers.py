from pkm_sim_commons import Pokemon

from pkm_sim_api.schemas.pokemon_schema import PokemonSchema


class PokemonMapper:

    def map_pk_to_schema(self, pkm: Pokemon) -> PokemonSchema:
        return PokemonSchema(**pkm.to_dict())