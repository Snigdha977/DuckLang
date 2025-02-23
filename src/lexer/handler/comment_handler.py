from .base import TokenHandler
from ..token_types import TokenType
from ..state import LexerState, Position

class CommentHandler(TokenHandler):
    """Handles both single-line and multi-line comments."""

    def can_handle(self, state):
        """Check if the current character starts a comment."""
        return state.match("#") or state.match("/*")

    def handle(self, state: LexerState, start_pos: Position):
        """Extracts and handles a comment token."""
        start_pos = state.position.copy()

        # Single-line comment (e.g., # This is a comment)
        if state.match("#"):
            state.advance()  # Skip #
            while not state.is_at_end() and not state.match("\n"):
                state.advance()
            return  # Ignore comment (do not store it)

        # Multi-line comment (e.g., /* This is a multi-line comment */)
        if state.match("/*"):
            state.advance(2)  # Skip /*
            while not state.is_at_end() and not state.match("*/"):
                state.advance()
            if state.match("*/"):
                state.advance(2)  # Skip */
            return  # Ignore comment (do not store it)

        # If we reach here, something went wrong
        raise ValueError(f"Unrecognized comment at position {start_pos}")
