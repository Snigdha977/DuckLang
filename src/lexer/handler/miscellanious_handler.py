from .base import TokenHandler
from ..token_types import TokenType
from ..state import LexerState,Position

class MiscellaneousHandler(TokenHandler):
    """Handles punctuation and special symbols."""

    TOKEN_MAP = {
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        ":": TokenType.COLON,
        ";": TokenType.SEMICOLON,
        "->": TokenType.ARROW,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        "[": TokenType.LEFT_BRACKET,
        "]": TokenType.RIGHT_BRACKET
    }

    def can_handle(self, state):
        """Check if the current character is a known miscellaneous symbol."""
        return state.current_char() in self.TOKEN_MAP 

    def handle(self, state:LexerState, start_pos: Position):
        """Extract and store the token."""
        start_pos = state.position.copy()

        
        raw_value = state.current_char()
        state.advance()

        token_type = self.TOKEN_MAP[raw_value]
        state.add_token(token_type, raw_value, start_pos, raw_value)
