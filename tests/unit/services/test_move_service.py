from unittest.mock import Mock

import pytest

from pkm_sim_api.services.move_service import MoveService


@pytest.fixture
def move_service():
    """Fixture que cria uma instância do PokemonService com mocks"""
    service = MoveService()
    service.repository = Mock()
    service.client = Mock()
    return service

class TestMoveService:

    def test_get_move_from_api(self, move_service):
        result = move_service.get_move_from_api('tackle')
        assert result is not None

    def test_get_move(self, move_service):
        result = move_service.get_move('tackle')
        assert result is not None
