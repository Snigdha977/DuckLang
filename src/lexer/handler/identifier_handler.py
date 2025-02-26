from ..token_types import TokenType
from ..state import LexerState, Position
from .base import TokenHandler

class IdentifierHandler(TokenHandler):
    """Handles identifiers and keywords like IF, FOR, RETURN, AND, OR."""

    keywords = {
        "for" : TokenType.FOR,
        "if" : TokenType.IF,
        "else" : TokenType.ELSE,
        "while" : TokenType.WHILE,
        "break" : TokenType.BREAK,
        "continue" : TokenType.CONTINUE,
        "return" : TokenType.RETURN,
        "and" : TokenType.AND,
        "or" : TokenType.OR,
        "not" : TokenType.NOT,
        "in" : TokenType.IN,
        "not_in" : TokenType.NOT_IN,
        "is" : TokenType.IS,
        "is_not" : TokenType.IS_NOT
        
    }

    def __init__(self):
        pass

    def can_handle(self, state: LexerState):
        """Check if the current character starts an identifier (letter or underscore)."""
        return state.current_char().isalpha() or state.current_char() == "_"
    
    def handle(self, state:LexerState, start_pos: Position):
        """Processes identifiers and keywords."""
        identifier = ""

        # Read while the character is alphanumeric or underscore
        while state.current_char().isalnum() or state.current_char() == "_":
            identifier += state.current_char()
            state.advance()

        # Determine token type keyword or identifier
        token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)

        # Store the token
        state.add_token(token_type, identifier, start_pos, identifier)