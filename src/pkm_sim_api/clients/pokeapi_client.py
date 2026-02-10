from .base_client import BaseAPIClient
from typing import Dict, Any


class PokeAPIClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://pokeapi.co/api/v2")

    async def get_pokemon(self, name_or_id: str | int) -> Dict[str, Any]:
        """Busca informações de um Pokémon"""
        return await self.get(f"/pokemon/{name_or_id}")

    async def get_pokemon_species(self, name_or_id: str | int):
        response = await self.get(f'/pokemon-species/{name_or_id}')
        return {
            'pokedex_num': response['id'],
            'name': response['name'],
            'evolution_chain_url': response['evolution_chain']['url'],
            'varieties': response['varieties']
        }

    async def get_evolution_chain(self, id: int):
        response = await self.get(f'/evolution-chain/{id}')
        return response

    async def get_ability(self, name_or_id: str | int) -> Dict[str, Any]:
        """Busca informações de uma habilidade"""
        return await self.get(f"/ability/{name_or_id}")

    async def get_move(self, name_or_id: str | int) -> Dict[str, Any]:
        """Busca informações de um movimento"""
        return await self.get(f"/move/{name_or_id}")

    async def get_item(self, name_or_id: str | int):
        return await self.get(f'/item/{name_or_id}')