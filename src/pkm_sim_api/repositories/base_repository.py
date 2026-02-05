from ..database import get_database


class BaseRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name

    async def create(self, data: dict):
        db = await get_database()
        db[self.collection_name].insert_one(data)

    async def update(self, pokedex_num: int, data: dict):
        db = await get_database()
        db[self.collection_name].update_one(
            {'pokedex_num': pokedex_num},
            {'$set': data}
        )

    async def delete(self, pokedex_num: int):
        db = await get_database()
        db[self.collection_name].delete_one(
            {'pokedex_num': pokedex_num}
        )

    async def find_by_id(self, id: int):
        db = await get_database()
        db[self.collection_name].find_one(
            {'id': id}
        )

    async def find_by_name(self, name: int):
        db = await get_database()
        db[self.collection_name].find_one(
            {'name': name}
        )
