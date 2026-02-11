from pkm_sim_commons import transform_stat_name
from pkm_sim_commons.models.move import Move

from pkm_sim_api.clients import PokeAPIClient
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.repositories.move_repository import MoveRepository


class MoveService:
    def __init__(self):
        self.client = PokeAPIClient()
        self.repository = MoveRepository()

    async def get_move(self, name: str):
        try:
            move = await self.repository.find_by_name(name)
            if move:
                return Move.from_dict(move)
            else:
                return await self.get_move_from_api(name)
        except Exception as e:
            raise PokemonSimAPIException(status_code=500, error_code=ErrorCode.POKE_SIM_GENERAL_ERROR, message='Error')


    async def get_move_from_api(self, name: str):
        async with self.client as client:
            try:
                json = await client.get_move(name)
                move = Move(
                    id=json['id'],
                    name=json['name'],
                    power=json['power'],
                    accuracy=json['accuracy'],
                    move_type=json['type']['name'],
                    effect_chance=json.get('effect_chance'),
                    damage_class=json['damage_class']['name'],
                    pp=json['pp'],
                    priority=json['priority'],
                    stat_changes=list([transform_stat_name(change['stat']['name']), change['change']] for change in json['stat_changes']),
                    target=json['target']['name'],
                    entries=[x['flavor_text'] for x in json['flavor_text_entries'] if x['language']['name'] == 'en'][0],
                    crit_rate=json['meta']['crit_rate'] if json['meta'] is not None else 0,
                    ailment=json['meta']['ailment']['name'] if json['meta'] is not None else None,
                    ailment_chance=json['meta']['ailment_chance'] if json['meta'] is not None else 0,
                    category=json['meta']['category']['name'] if json['meta'] is not None else None,
                    drain=json['meta']['drain'] if json['meta'] is not None else 0,
                    flinch_chance=json['meta']['flinch_chance'] if json['meta'] is not None else 0,
                    healing=json['meta']['healing'] if json['meta'] is not None else 0,
                    min_hits=json['meta']['min_hits'] if json['meta'] is not None else None,
                    max_hits=json['meta']['max_hits'] if json['meta'] is not None else None,
                    min_turns=json['meta']['min_turns'] if json['meta'] is not None else None,
                    max_turns=json['meta']['max_turns'] if json['meta'] is not None else None,
                    stat_chance=json['meta']['stat_chance'] if json['meta'] is not None else 0
                )
                await self.repository.create(move.__dict__)
                return move.to_dict()
            except Exception as e:
                raise PokemonSimAPIException(message=f'Error while saving move {name} at mongo database', status_code=500, error_code=ErrorCode.DATA_BASE_ERROR)