from .base_repository import BaseRepository
from ..database import get_database

class PokemonRepository(BaseRepository):
    def __init__(self, collection_name=None):
        super().__init__(collection_name='pokemon')

    async def find_by_pokedex_num(self, pokedex_num: int):
        db = await get_database()
        db[self.collection_name].find_one(
            {'pokedex_num': pokedex_num}
        )


