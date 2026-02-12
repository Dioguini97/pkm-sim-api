from .pokemon_router import router as pokemon_router
from .competitive_pokemon_router import router as competitive_router
from .move_router import router as move_router
from .item_router import router as item_router
from .auth_router import router as auth_router

__all__ = ['pokemon_router', 'item_router', 'competitive_router', 'move_router', 'auth_router']