from pkm_sim_commons.models.ability import Ability

from pkm_sim_api.clients import PokeAPIClient
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.repositories.ability_repository import AbilityRepository


class AbilityService:
    def __init__(self):
        self.client = PokeAPIClient()
        self.repository = AbilityRepository()

    async def get_ability(self, name) -> Ability:
        try:
            abl = await self.repository.find_by_name(name)
            if abl:
                return Ability.from_dict(abl)
            else:
                return await self.get_ability_from_api(name)
        except:
            raise PokemonSimAPIException(
                message=f'Ability {name} not found', status_code=404, error_code=ErrorCode.DATA_BASE_ERROR)

    async def get_ability_from_api(self, name: str):
        async with self.client as client:
            try:
                json = await client.get_ability(name)
                ability = Ability(
                    id=json['id'], name=json['name'], description=[effect_entry['effect'] for effect_entry in json['effect_entries'] if effect_entry['language']['name'] == 'en'][0],
                )
                await self.repository.create(ability.__dict__)
                return ability.to_dict()
            except PokemonSimAPIException as e:
                raise PokemonSimAPIException(message=e.message, status_code=e.status_code)
