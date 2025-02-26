from ..token_types import TokenType
from .base import TokenHandler
from ..state import LexerState,Position

class StringHandler(TokenHandler):
    """Handles the detection and tokenization of string literals."""

    def can_handle(self, state):
        """Check if the current character starts a string (single or double quote)."""
        return state.current_char() in ('"', "'")
    
    def handle(self, state:LexerState, start_pos: Position):
        """extract a string token from input"""
        start_pos = state.position.copy()
        quote_char = state.current_char() # Store the opening quote type (' or ")
        state.advance()

        raw_value = ""
        while state.current_char() and state.current_char() != quote_char:
            raw_value += state.current_char()
            state.advance()

        if not state.current_char():
            raise SyntaxError(f"Unterminated string starting at {start_pos}")
        
        state.advance()

        state.add_token(TokenType.STRING, raw_value, start_pos, quote_char+raw_value+quote_char)
