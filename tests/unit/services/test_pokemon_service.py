import pytest
from unittest.mock import Mock

from pkm_sim_api.clients import PokeAPIClient
from pkm_sim_api.services.pokemon_service import PokemonService


@pytest.fixture
def pokemon_service():
    """Fixture que cria uma instância do PokemonService com mocks"""
    service = PokemonService()
    service.repository = Mock()
    service.client = Mock()
    return service


@pytest.fixture
def mock_pokemon_data():
    """Dados de exemplo de um Pokémon da API"""
    return {
        'id': 25,
        'name': 'pikachu',
        'types': [{'type': {'name': 'electric'}}],
        'base_stats': {'hp': 35, 'attack': 55},
        'abilities': [{'ability': {'name': 'static'}}],
        'height': 4,
        'weight': 60,
        'move_list': ['thunderbolt', 'quick-attack'],
        'img_url': 'https://example.com/pikachu.png',
        'crie_url': 'https://example.com/pikachu_cry.mp3'
    }


@pytest.fixture
def mock_species_data():
    """Dados de exemplo da espécie do Pokémon"""
    return {
        'name': 'pikachu',
        'evolution_chain_url': 'https://pokeapi.co/api/v2/evolution-chain/10/',
        'varieties': [
            {'pokemon': {'name': 'pikachu'}},
            {'pokemon': {'name': 'pikachu-gmax'}}
        ]
    }


@pytest.fixture
def mock_evolution_chain_can_evolve():
    """Cadeia de evolução onde o Pokémon pode evoluir"""
    return {
        'chain': {
            'species': {'name': 'pichu'},
            'evolves_to': [{
                'species': {'name': 'pikachu'},
                'evolves_to': [{
                    'species': {'name': 'raichu'},
                    'evolves_to': []
                }]
            }]
        }
    }


@pytest.fixture
def mock_evolution_chain_cannot_evolve():
    """Cadeia de evolução onde o Pokémon não pode evoluir"""
    return {
        'chain': {
            'species': {'name': 'pichu'},
            'evolves_to': [{
                'species': {'name': 'pikachu'},
                'evolves_to': [{
                    'species': {'name': 'raichu'},
                    'evolves_to': []  # Raichu não evolui mais
                }]
            }]
        }
    }

class TestCanItEvolve:
    """Testes para o método can_it_evolve"""

    def test_pokemon_at_chain_start_can_evolve(self, pokemon_service):
        """Testa se um Pokémon no início da cadeia pode evoluir"""
        evo_chain = {
            'chain': {
                'species': {'name': 'pichu'},
                'evolves_to': [{
                    'species': {'name': 'pikachu'},
                    'evolves_to': []
                }]
            }
        }

        result = pokemon_service.can_it_evolve(evo_chain, 'pichu')
        assert result is True

    def test_pokemon_at_chain_start_cannot_evolve(self, pokemon_service):
        """Testa se um Pokémon no início da cadeia que não evolui"""
        evo_chain = {
            'chain': {
                'species': {'name': 'ditto'},
                'evolves_to': []
            }
        }

        result = pokemon_service.can_it_evolve(evo_chain, 'ditto')
        assert result is False

    def test_pokemon_in_middle_can_evolve(self, pokemon_service, mock_evolution_chain_can_evolve):
        """Testa se um Pokémon no meio da cadeia pode evoluir"""
        result = pokemon_service.can_it_evolve(mock_evolution_chain_can_evolve, 'pikachu')
        assert result is True

    def test_pokemon_at_end_cannot_evolve(self, pokemon_service, mock_evolution_chain_cannot_evolve):
        """Testa se um Pokémon no final da cadeia não pode evoluir"""
        result = pokemon_service.can_it_evolve(mock_evolution_chain_cannot_evolve, 'raichu')
        assert result is False

    def test_pokemon_not_in_chain(self, pokemon_service, mock_evolution_chain_can_evolve):
        """Testa quando o Pokémon não está na cadeia de evolução"""
        result = pokemon_service.can_it_evolve(mock_evolution_chain_can_evolve, 'charizard')
        assert result is False

class TestEdgeCases:
    """Testes de casos extremos e edge cases"""

    def test_evolution_chain_with_multiple_branches(self, pokemon_service):
        """Testa cadeia de evolução com múltiplas ramificações (ex: Eevee)"""
        evo_chain = {
            'chain': {
                'species': {'name': 'eevee'},
                'evolves_to': [
                    {'species': {'name': 'vaporeon'}, 'evolves_to': []},
                    {'species': {'name': 'jolteon'}, 'evolves_to': []},
                    {'species': {'name': 'flareon'}, 'evolves_to': []}
                ]
            }
        }

        # Eevee pode evoluir
        assert pokemon_service.can_it_evolve(evo_chain, 'eevee') is True

        # Evoluções finais não podem evoluir
        assert pokemon_service.can_it_evolve(evo_chain, 'vaporeon') is False
        assert pokemon_service.can_it_evolve(evo_chain, 'jolteon') is False

    def test_empty_evolution_chain(self, pokemon_service):
        """Testa com cadeia de evolução vazia"""
        evo_chain = {
            'chain': {
                'species': {'name': 'unknown'},
                'evolves_to': []
            }
        }

        result = pokemon_service.can_it_evolve(evo_chain, 'unknown')
        assert result is False