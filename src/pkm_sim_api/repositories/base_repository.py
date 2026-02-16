from pkm_sim_api.configs.database import get_database
from pkm_sim_api.configs.pkm_sim_api_exception import PokemonSimAPIException


class BaseRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name

    async def create(self, data):
        db = await get_database()
        try:
            result = await db[self.collection_name].insert_one(data)
        except PokemonSimAPIException as e:
            raise PokemonSimAPIException(
                f'Error trying to save {data} to Mongo DB!', 500
            )

    async def update(self, pokedex_num: int, data: dict):
        db = await get_database()
        result = await db[self.collection_name].update_one(
            {'pokedex_num': pokedex_num},
            {'$set': data}
        )
        return result.raw_result

    async def delete(self, pokedex_num: int):
        db = await get_database()
        result = await db[self.collection_name].delete_one(
            {'pokedex_num': pokedex_num},
            {'_id': 0}
        )
        return result.raw_result

    async def find_by_id(self, id: int):
        db = await get_database()
        result = await db[self.collection_name].find_one(
            {'id': id},
            {'_id': 0}
        )
        return result

    async def find_by_name(self, name: str):
        db = await get_database()
        result = await db[self.collection_name].find_one(
            {'name': name},
            {'_id': 0}
        )
        return result

    async def find_all(self):
        db = await get_database()
        result = await db[self.collection_name].find({},
            {'_id': 0, 'name': 1}).to_list(100)
        return result
