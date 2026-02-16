from pkm_sim_api.repositories.base_repository import BaseRepository


class AbilityRepository(BaseRepository):
    def __init__(self, collection_name=None):
        super().__init__(collection_name='ability')