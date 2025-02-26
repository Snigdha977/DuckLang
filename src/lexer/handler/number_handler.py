import re
from ..token_types import TokenType
from .base import TokenHandler
from ..state import LexerState,Position

class NumberHandler(TokenHandler):
    """Handles the detection and tokenization of integers and floating-point numbers."""

    def can_handle(self, state):
        """Check if the next character is a digit (0-9)."""
        return state.current_char().isdigit()
    
    def handle(self, state:LexerState, start_pos: Position):
        """Extracts a number token (integer or float) from the input."""
        start_pos = state.position.copy()
        raw_value = ""

        while state.current_char() and (state.current_char().isdigit() or state.current_char() == "."):
            raw_value += state.current_char()
            state.advance()

        # Determine if it is an integer or float
        if "." in raw_value:
            token_type = TokenType.FLOAT
        else:
            token_type = TokenType.INTEGER

        # Store the token
        state.add_token(token_type, raw_value, start_pos, raw_value)

