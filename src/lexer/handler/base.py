from abc import ABC, abstractmethod
from ..state import LexerState, Position

class TokenHandler(ABC):
    """Base class for all token handlers."""
    
    @abstractmethod
    def can_handle(self, state: LexerState) -> bool:
        """Check if the handler can process the current character."""
        pass

    @abstractmethod
    def handle(self, state: LexerState, start_pos: Position) -> None:
        """Process the token and update state."""
        pass
