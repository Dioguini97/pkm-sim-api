from enum import Enum

class ErrorCode(Enum):
    DATA_BASE_ERROR = 'Data Base Error'
    POKE_API_ERROR = 'PokeAPI Error'
    POKE_SIM_GENERAL_ERROR = 'Pokemon Simulator API General Error'
    FEING_CLIENT_ERROR = 'Feing Client Error'

class PokemonSimAPIException(Exception):
    def __init__(self, message: str, *, status_code: int = 400, error_code: ErrorCode=None, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

    def __repr__(self):
        return {
            'message': self.message,
            'status_code': self.status_code,
            'error_code': self.error_code.value,
            'details': self.details
        }

