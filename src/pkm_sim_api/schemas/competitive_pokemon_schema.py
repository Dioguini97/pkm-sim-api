from pydantic import BaseModel
from typing import List, Dict, Optional
from .pokemon_schema import PokemonSchema


class CompetitivePokemonSchema(BaseModel):
    user: str
    name: str
    nickname: Optional[str] = None
    ability: str
    nature: str
    moves: List[str]
    pkm: PokemonSchema

    ivs: Optional[Dict[str, int]] = None
    evs: Optional[Dict[str, int]] = None

    item: Optional[str] = None
    level: int = 50
