from pkm_sim_api.repositories.base_repository import BaseRepository


class ItemRepository(BaseRepository):
    def __init__(self, collection_name=None):
        super().__init__('item')