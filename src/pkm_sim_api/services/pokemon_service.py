from ..clients import PokeAPIClient
from ..models.pkm_sim_api_exception import PokemonSimAPIException
from ..repositories import PokemonRepository
from pkm_sim_commons import Pokemon

class PokemonService:
    def __init__(self):
        self.client = PokeAPIClient()
        self.repository = PokemonRepository()

    def get_pokemon(self, name: str) -> Pokemon:
        try:
            self.repository.find_by_name(name)
        except:
            self.get_pokemon_from_api(name)

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
                pkm = client.get_pokemon(name_or_id)
                specie = client.get_pokemon_species(name_or_id)
                evo_chain = client.get_evolution_chain(specie['evolution_chain_url'].split('/')[-2])
                pkm['can_evolve'] = self.can_it_evolve(evo_chain, specie['name'])
                pkm['varieties'] = specie['varieties']
                pokemon = Pokemon(
                    pokedex_num=pkm['id'], name=pkm['name'], can_evolve=pkm['can_evolve'],
                    types=pkm['types'], base_stats=pkm['base_stats'], abilities=pkm['abilities'],
                    height=pkm['height'], weight=pkm['weight'], move_list=pkm['move_list'],
                    img_url=pkm['img_url'], crie_url=pkm['crie_url'], varieties=pkm['varieties']
                )
                self.repository.create(pokemon)
                return pokemon
            except PokemonSimAPIException as e:
                raise PokemonSimAPIException(f'Error getting Pokemon: {name_or_id}')