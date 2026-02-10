from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class PokemonSchema(BaseModel):
    pokedex_num: int
    name: str
    types: List[str]
    base_stats: Dict[str, int]
    abilities: List[str]
    height: float
    weight: float
    move_list: List[str]
    img_url: str
    crie_url: Optional[str] = None
    can_evolve: Optional[bool] = None
    varieties: Optional[List[str]] = None
