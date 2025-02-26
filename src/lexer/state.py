from src.lexer.token_types import Token

class Position:
    """Tracks the position (index, line, column) in the source code."""
    def __init__(self, index=0, line=1, column=1):
        self.index = index
        self.line = line
        self.column = column

    def copy(self):
        """Returns a copy of the current position."""
        return Position(self.index, self.line, self.column)

    def advance(self, char):
        """Advances the position, updating line and column numbers."""
        self.index += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

class LexerState:
    """Manages the current state of the lexer, including character position and tokens."""
    def __init__(self, source: str):
        self.source = source
        self.position = Position()
        self.tokens = []
        # Don't store initial character, get it from source when needed
        
    def current_char(self):
        """Returns the current character being processed or None if at end."""
        if self.position.index >= len(self.source):
            return None
        return self.source[self.position.index]

    def has_more_chars(self) -> bool:
        """Checks if there are more characters left to process."""
        return self.position.index < len(self.source)
    
    def next_char(self):
        """Returns the next character in the source code or None if at end."""
        next_idx = self.position.index + 1
        if next_idx >= len(self.source):
            return None
        return self.source[next_idx]

    def advance(self, steps=1):
        """Moves forward in the source code by a given number of characters."""
        for _ in range(steps):
            if self.has_more_chars():
                self.position.advance(self.current_char())

    def peek(self, offset=1):
        """Looks ahead in the source without advancing the position."""
        peek_index = self.position.index + offset
        if peek_index >= len(self.source):
            return None
        return self.source[peek_index]
    
    def match(self, text):
        """Checks if the next characters match the given text and advances if true."""
        if self.source[self.position.index:self.position.index + len(text)] == text:
            for _ in range(len(text)):  
                self.advance()
            return True
        return False

    def add_token(self, token_type, value, start_pos, raw):
        """Creates and stores a new token."""
        token = Token(
            token_type=token_type,
            value=value,
            start_pos=start_pos,
            end_pos=self.position.copy(),
            raw=raw
        )
        self.tokens.append(token)