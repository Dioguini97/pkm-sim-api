from enum import Enum

class ErrorCode(Enum):
    DATA_BASE_ERROR = 'Data Base Error'

class PokemonSimAPIException(Exception):
    def __init__(self, message: str, *, status_code: int = 400, error_code: ErrorCode=None, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super.__init__(message)

