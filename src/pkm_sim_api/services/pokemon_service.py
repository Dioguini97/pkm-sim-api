from ..clients import PokeAPIClient
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException
from ..repositories import PokemonRepository
from pkm_sim_commons import Pokemon, transform_stat_name, PokemonType


class PokemonService:
    def __init__(self):
        self.client = PokeAPIClient()
        self.repository = PokemonRepository()

    async def get_pokemon(self, name: str) -> Pokemon:
        try:
            pkm = await self.repository.find_by_name(name)
            if pkm:
                return Pokemon(
                    pokedex_num=pkm['pokedex_num'], name=pkm['name'], can_evolve=pkm['can_evolve'],
                    types=[PokemonType(_type) for _type in pkm['types']], base_stats=pkm['base_stats'],
                    abilities=[abl for abl in pkm['abilities']],
                    height=pkm['height'], weight=pkm['weight'], move_list=pkm['move_list'],
                    img_url=pkm['img_url'], crie_url=pkm['crie_url'], varieties=pkm['varieties']
                )
            return await self.get_pokemon_from_api(name)
        except PokemonSimAPIException as e:
            raise PokemonSimAPIException(
                f'Pokemon com nome {name} não existe!', status_code=500
            )

    def can_it_evolve(self, evo_chain, pkm_name) -> bool:
        """Checks if the Pokémon can evolve based on cached species data."""
        if evo_chain['chain']['species']['name'] == pkm_name:
            if len(evo_chain['chain']['evolves_to']) > 0:
                return True
            else:
                return False
        else:
            for evolution in evo_chain['chain']['evolves_to']:
                if evolution['species']['name'] == pkm_name:
                    if len(evolution['evolves_to']) > 0:
                        return True
                    else:
                        return False
            return False

    async def get_pokemon_from_api(self, name_or_id: str | int):
        if type(name_or_id) == str:
            name_or_id = name_or_id.split('-')[0]
        async with self.client as client:
            try:
                pkm = await client.get_pokemon(name_or_id)
                specie = await client.get_pokemon_species(name_or_id)
                evo_chain = await client.get_evolution_chain(specie['evolution_chain_url'].split('/')[-2])
                pokemon = Pokemon(
                    pokedex_num=pkm['id'], name=pkm['name'], can_evolve=self.can_it_evolve(evo_chain, specie['name']),
                    types=[PokemonType(_type['type']['name']) for _type in pkm['types']], base_stats={transform_stat_name(stat['stat']['name']): stat['base_stat'] for stat in pkm['stats']},
                    abilities=[abl['ability']['name'] for abl in pkm['abilities']],
                    height=pkm['height'], weight=pkm['weight'], move_list=[move['move']['name'] for move in pkm['moves']],
                    img_url=pkm['sprites']['front_default'], crie_url=pkm['cries']['latest'], varieties=specie['varieties']
                )
                await self.repository.create(pokemon.__dict__)
                return pokemon
            except PokemonSimAPIException as e:
                raise PokemonSimAPIException(f'Error getting Pokemon: {name_or_id}')
