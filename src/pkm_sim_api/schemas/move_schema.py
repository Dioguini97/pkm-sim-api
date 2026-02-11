from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class MoveSchema(BaseModel):
    name: str
    power: int
    move_type: str
    accuracy: int
    effect_chance: int  # e.g., 20% chance of lower spdef
    damage_class: str  # e.g., Physical, Special, Status
    pp: int
    priority: int
    stat_changes: List[Any]  # e.g., [['spdef', -1]]
    target: str  # e.g., 'selected-pokemon', 'all-opponents'
    entries: str  # e.g., "May lower the target's Special Defense by 1 stage."
    id: int
    ailment: str
    ailment_chance: int
    category: str
    crit_rate: int
    drain: int
    flinch_chance: int
    healing: int
    min_hits: int
    max_hits: int
    min_turns: int
    max_turns: int
    stat_chance: int
    _id: str