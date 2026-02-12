from pkm_sim_api.configs.database import get_database
from pkm_sim_api.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, collection_name=None):
        super().__init__(collection_name='user')

    async def find_by_username(self, username: str):
        db = await get_database()
        return await db[self.collection_name].find_one(
            {'username': username}
        )
