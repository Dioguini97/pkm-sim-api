from pkm_sim_commons import ItemAttribute
from pkm_sim_commons.models.item import Item

from pkm_sim_api.clients import PokeAPIClient
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException, ErrorCode
from pkm_sim_api.repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self):
        self.client = PokeAPIClient()
        self.repository = ItemRepository()

    async def get_item(self, name: str) -> Item:
        try:
            item = await self.repository.find_by_name(name)
            if item:
                return Item.from_dict(item)
            else:
                return await self.get_item_from_api(name)
        except Exception as e:
            raise PokemonSimAPIException(message=f'Unable to get item {item}\n{e}', status_code=404, error_code=ErrorCode.DATA_BASE_ERROR)

    async def get_item_from_api(self, name: str):
        async with self.client as client:
            try:
                json = await client.get_item(name)
                item = Item(
                    name=json['name'],
                    id=json['id'],
                    img_url=json['sprites']['default'],
                    attributes=[att['name'] for att in json['attributes']],
                    category=json['category']['name'],
                    fling_power=json['fling_power'],
                    fling_effect=json['fling_effect']['name'] if json['fling_effect'] else None,
                    description=[entry['effect'] for entry in json['effect_entries'] if entry['language']['name'] == 'en'][0]
                )
                await self.repository.create(item.__dict__)
                return item.to_dict()
            except:
                raise PokemonSimAPIException(message='Something gone wrong with PokeAPI', status_code=500, error_code=ErrorCode.FEING_CLIENT_ERROR)