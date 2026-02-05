import pytest
import asyncio
import os
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Define que estamos em modo de teste ANTES de importar
env_path = Path(__file__).parent.parent / '.env.test'
load_dotenv(dotenv_path=env_path, override=True)
os.environ['TESTING'] = '1'

from src.pkm_sim_api.main import app
from src.pkm_sim_api.database import get_database
from src.pkm_sim_api.config import settings


@pytest.fixture
def client():
    """Cliente síncrono para testar endpoints"""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Cliente assíncrono para testes assíncronos"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Database de teste (limpa após cada teste)"""
    client = AsyncIOMotorClient(settings.mongodb_url)
    db_name = f"test_{settings.database_name}"
    db = client[db_name]

    yield db

    # Cleanup: apaga a database de teste
    await client.drop_database(db_name)
    client.close()


@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_pokemon_data():
    """Dados de exemplo de um Pokémon"""
    return {
        "pokedex_num": 25,
        "name": "pikachu",
        "types": ["electric"],
        "base_stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special_attack": 50,
            "special_defense": 50,
            "speed": 90
        },
        "abilities": ["static", "lightning-rod"],
        "height": 4,
        "weight": 60,
        "move_list": ["thunderbolt", "quick-attack"],
        "img_url": "https://example.com/pikachu.png"
    }