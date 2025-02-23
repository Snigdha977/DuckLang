from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Tuple, Optional, Set
import re
from lib.syntax import syntax

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int, context: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.context = context
        super().__init__(f"Line {line}, Column {column}: {message}\nContext: {context}")

class TokenType(Enum):

    # custom tokens
    PRINT_COMMAND = "PRINT_COMMAND"
    VARIABLE_DECLARE = "VARIABLE_DECLARE"

    # Basic types
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BYTES = "BYTES"
    BOOLEAN = "BOOLEAN"
    NONE = "NONE"
    
    # Collections
    LIST_START = "LIST_START"
    LIST_END = "LIST_END"
    TUPLE_START = "TUPLE_START"
    TUPLE_END = "TUPLE_END"
    DICT_START = "DICT_START"
    DICT_END = "DICT_END"
    SET_START = "SET_START"
    SET_END = "SET_END"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    FLOOR_DIVIDE = "FLOOR_DIVIDE"
    POWER = "POWER"
    MODULO = "MODULO"
    
    # Comparisons
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Logical
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IN = "IN"
    NOT_IN = "NOT_IN"
    IS = "IS"
    IS_NOT = "IS_NOT"
    
    # Comprehension
    FOR = "FOR"
    IF = "IF"
    ELSE = "ELSE"
    
    # Other
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    ASSIGN = "ASSIGN"
    ARROW = "ARROW"
    LAMBDA = "LAMBDA"
    WALRUS = "WALRUS"

    # token types for control flow
    ELIF = "ELIF"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    
    # Scope and statement tokens
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    BLOCK_START = "BLOCK_START"
    BLOCK_END = "BLOCK_END"
    SEMICOLON = "SEMICOLON"
    LINE_CONTINUATION = "LINE_CONTINUATION"


@dataclass
class Position:
    line: int
    column: int
    index: int
    file: str = "<unknown>"

    def advance(self, char: str = '') -> None:
        self.index += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

    def copy(self) -> 'Position':
        return Position(self.line, self.column, self.index, self.file)

@dataclass
class Token:
    type: TokenType
    value: Any
    start_pos: Position  # Keep this for internal use
    end_pos: Position    # Keep this for internal use
    raw: str
    context: str = ""
    position: int = field(init=False)  # Add this field

    def __post_init__(self):
        if not self._validate():
            raise ValueError(f"Invalid token value for type {self.type}: {self.value}")
        # Set position to the character index
        self.position = self.start_pos.index

    def _validate(self) -> bool:
        try:
            if self.type == TokenType.INTEGER:
                return isinstance(self.value, int)
            elif self.type == TokenType.FLOAT:
                return isinstance(self.value, float)
            elif self.type == TokenType.STRING:
                return isinstance(self.value, str)
            elif self.type == TokenType.BOOLEAN:
                return isinstance(self.value, bool)
            elif self.type == TokenType.NONE:
                return self.value is None
            return True
        except Exception:
            return False

class LexerState:
    def __init__(self, source: str, filename: str = "<unknown>"):
        self.source = source
        self.position = Position(1, 1, 0, filename)
        self.current_char = source[0] if source else None
        self.tokens: List[Token] = []
        self.indentation_stack: List[int] = [0]
        self.nesting_levels = {
            '(': 0, '[': 0, '{': 0
        }
        self.context_window = 50  # Characters of context to store for error messages



    def advance(self) -> None:
        try:
            self.position.advance(self.current_char)
            self.current_char = self.source[self.position.index] if self.position.index < len(self.source) else None
        except IndexError:
            self.current_char = None

    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.position.index + offset
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def get_context(self) -> str:
        start = max(0, self.position.index - self.context_window)
        end = min(len(self.source), self.position.index + self.context_window)
        return self.source[start:end]

class ComplexLexer:
    def __init__(self):
        
        self.print_command = syntax.get("PRINT_COMMAND", "quack")
        self.var_declare_command = syntax.get("VARIABLE_DECLARE", "let")
        self._init_patterns()
        self._init_keywords()
        self._init_operators()
        

    def _init_patterns(self):
        self.patterns = {
            'number': re.compile(r'''
                (?:\d*\.)?\d+(?:[eE][+-]?\d+)?  # Regular numbers and scientific notation
                |
                0[xX][0-9a-fA-F]+               # Hex numbers
                |
                0[bB][01]+                      # Binary numbers
                |
                0[oO][0-7]+                     # Octal numbers
            ''', re.VERBOSE),
            'identifier': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
            'string': re.compile(r'''
                (?:
                    [fF]?                           # Optional f-string prefix
                    (?:
                        |
                        "(?:\\.|[^"\\])*"          # Double quoted string
                        |
                        '(?:\\.|[^'\\])*'          # Single quoted string
                    )
                )
                |
                (?:
                    [rR]                           # Raw string prefix
                    (?:
                        
                        |
                        "(?:\\.|[^"\\])*"          
                        |
                        '(?:\\.|[^'\\])*'          
                    )
                )
            ''', re.VERBOSE),
            # 'print_command': re.compile(
            #     rf'\b{re.escape(self.print_command)}\s*\(((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*)\)'
            # ),

            'print_command': re.compile(
            rf'{re.escape(self.print_command)}\s*\(' # Just match 'quack('
        ),
            # 'var_declare': re.compile(
            #     rf'\b{re.escape(self.var_declare_command)}\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*((?:[^;\n]+|\[(?:[^\[\]]+|\[[^\[\]]*\])*\])*)'
            # ),
            'bytes': re.compile(r'[bB](?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')'),
            'whitespace': re.compile(r'\s+'),
            'comment': re.compile(r'#[^\n]*'),
        }
    def _init_keywords(self):
        self.keywords = {
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            'in': TokenType.IN,
            'is': TokenType.IS,
            'None': TokenType.NONE,
            'True': TokenType.BOOLEAN,
            'False': TokenType.BOOLEAN,
            'lambda': TokenType.LAMBDA,
            'for': TokenType.FOR,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'elif': TokenType.ELIF,
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
        }

    def _init_operators(self):
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '//': TokenType.FLOOR_DIVIDE,
            '**': TokenType.POWER,
            '%': TokenType.MODULO,
            '=': TokenType.ASSIGN,
            '==': TokenType.EQUALS,
            '!=': TokenType.NOT_EQUALS,
            '<': TokenType.LESS_THAN,
            '>': TokenType.GREATER_THAN,
            '<=': TokenType.LESS_EQUAL,
            '>=': TokenType.GREATER_EQUAL,
            ':=': TokenType.WALRUS,
            '->': TokenType.ARROW,
        }

    def tokenize(self, source: str, filename: str = "<unknown>") -> List[Token]:
        state = LexerState(source, filename)
        
        try:
            while state.current_char is not None:
                start_pos = state.position.copy()

                # Handle line start indentation
                if state.position.column == 1:
                    self._handle_indentation(state)

                # Handle line continuation
                if state.current_char == '\\' and state.peek() == '\n':
                    self._add_token(state, TokenType.LINE_CONTINUATION, '\\', start_pos, '\\')
                    state.advance()  # Skip backslash
                    state.advance()  # Skip newline
                    continue

                # Skip comments
                if state.current_char == '#':
                    self._handle_comment(state)
                    continue

                # Handle whitespace and indentation
                if state.current_char.isspace():
                    self._handle_whitespace(state)
                    continue

                # Check for print command
                if state.source[state.position.index:].startswith(self.print_command):
                    self._handle_print_command(state, start_pos)
                    continue

                # Check for variable declaration
                if state.source[state.position.index:].startswith(self.var_declare_command):
                    self._handle_var_declaration(state, start_pos)
                    continue

                # Handle numbers
                if state.current_char.isdigit() or state.current_char == '.':
                    self._handle_number(state, start_pos)
                    continue

                # Handle strings
                if state.current_char in '"\'':
                    self._handle_string(state, start_pos)
                    continue

                # Handle bytes
                if state.current_char in 'bB' and state.peek() in '"\'':
                    self._handle_bytes(state, start_pos)
                    continue

                # Handle identifiers and keywords
                if state.current_char.isalpha() or state.current_char == '_':
                    self._handle_identifier(state, start_pos)
                    continue

                # Add handling for compound statements
                if state.current_char.isalpha():
                    self._handle_compound_statement(state, start_pos)
                    continue

                # Handle operators and delimiters
                self._handle_operator_or_delimiter(state, start_pos)

            # Handle any remaining dedents at end of file
            while len(state.indentation_stack) > 1:
                state.indentation_stack.pop()
                self._add_token(state, TokenType.BLOCK_END, 'block_end', state.position, '')
                self._add_token(state, TokenType.DEDENT, 0, state.position, "")

        except Exception as e:
            if not isinstance(e, LexerError):
                context = state.get_context()
                raise LexerError(str(e), state.position.line, state.position.column, context)
            raise

        # Validate final state
        self._validate_final_state(state)
        return state.tokens
    
    def _handle_indentation(self, state: LexerState) -> None:
        current_indent = 0
        while state.current_char == ' ':
            current_indent += 1
            state.advance()
            
        if current_indent > state.indentation_stack[-1]:
            state.indentation_stack.append(current_indent)
            self._add_token(state, TokenType.INDENT, current_indent, state.position, " " * current_indent)
            self._add_token(state, TokenType.BLOCK_START, 'block_start', state.position, '')
        elif current_indent < state.indentation_stack[-1]:
            while current_indent < state.indentation_stack[-1]:
                state.indentation_stack.pop()
                self._add_token(state, TokenType.BLOCK_END, 'block_end', state.position, '')
                self._add_token(state, TokenType.DEDENT, current_indent, state.position, "")
                if current_indent > state.indentation_stack[-1]:
                    raise LexerError("Invalid dedent level", 
                                   state.position.line, 
                                   state.position.column,
                                   state.get_context())

    def _handle_comment(self, state: LexerState) -> None:
        while state.current_char and state.current_char != '\n':
            state.advance()

    def _handle_whitespace(self, state: LexerState) -> None:
        while state.current_char and state.current_char.isspace():
            state.advance()
    
    def _handle_print_command(self, state: LexerState, start_pos: Position) -> None:
        # First, handle the quack keyword itself
        command_str = self.print_command
        self._add_token(
            state,
            TokenType.PRINT_COMMAND,
            command_str,
            start_pos,
            command_str
        )
        
        # Advance past 'quack'
        for _ in range(len(command_str)):
            state.advance()
            
        # Skip any whitespace
        while state.current_char and state.current_char.isspace():
            state.advance()
            
        # Handle the opening parenthesis
        if state.current_char == '(':
            state.advance()  # move past the opening parenthesis
            
            # Skip any whitespace after the parenthesis
            while state.current_char and state.current_char.isspace():
                state.advance()
            
            # Now handle the argument based on its type
            if state.current_char:
                arg_start_pos = state.position.copy()
                if state.current_char.isdigit():
                    # Handle numeric argument
                    self._handle_number(state, arg_start_pos)
                elif state.current_char in '"\'':
                    # Handle string argument
                    self._handle_string(state, arg_start_pos)
                elif state.current_char.isalpha() or state.current_char == '_':
                    # Handle identifier argument
                    self._handle_identifier(state, arg_start_pos)
            
            # Look for and handle the closing parenthesis
            while state.current_char and state.current_char.isspace():
                state.advance()
                
            if state.current_char == ')':
                state.advance()
            else:
                raise LexerError(
                    "Expected closing parenthesis",
                    state.position.line,
                    state.position.column,
                    state.get_context()
                )

    def _handle_var_declaration(self, state: LexerState, start_pos: Position) -> None:
        # Match just the 'let' and identifier part
        var_pattern = re.compile(rf'\b{re.escape(self.var_declare_command)}\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*')
        match = var_pattern.match(state.source[state.position.index:])
        
        if match:
            # Add variable declaration token
            self._add_token(
                state,
                TokenType.VARIABLE_DECLARE,
                self.var_declare_command,
                start_pos,
                self.var_declare_command
            )
            
            # Add identifier token
            identifier_pos = Position(
                start_pos.line,
                start_pos.column + len(self.var_declare_command) + 1,
                start_pos.index + len(self.var_declare_command) + 1,
                start_pos.file
            )
            self._add_token(
                state,
                TokenType.IDENTIFIER,
                match.group(1),
                identifier_pos,
                match.group(1)
            )
            
            # Add equals token
            equals_pos = Position(
                identifier_pos.line,
                identifier_pos.column + len(match.group(1)) + 1,
                identifier_pos.index + len(match.group(1)) + 1,
                start_pos.file
            )
            self._add_token(
                state,
                TokenType.ASSIGN,
                "=",
                equals_pos,
                "="
            )
            
            # Advance past the 'let', identifier, and equals sign
            for _ in range(len(match.group(0))):
                state.advance()
                
            # Now handle the expression
            expression_pos = state.position.copy()
            self._handle_expression(state, expression_pos)

    def _handle_number(self, state: LexerState, start_pos: Position) -> None:
        num_str = ''
        while state.current_char and (state.current_char.isdigit() or state.current_char in '.eE+-xXbBoO'):
            num_str += state.current_char
            state.advance()

        try:
            if '.' in num_str or 'e' in num_str.lower():
                value = float(num_str)
                token_type = TokenType.FLOAT
            else:
                if num_str.startswith(('0x', '0X')):
                    value = int(num_str, 16)
                elif num_str.startswith(('0b', '0B')):
                    value = int(num_str, 2)
                elif num_str.startswith(('0o', '0O')):
                    value = int(num_str, 8)
                else:
                    value = int(num_str)
                token_type = TokenType.INTEGER

            self._add_token(state, token_type, value, start_pos, num_str)
        except ValueError:
            raise LexerError(f"Invalid number format: {num_str}", 
                           start_pos.line, 
                           start_pos.column,
                           state.get_context())

    def _handle_string(self, state: LexerState, start_pos: Position) -> None:
        is_raw = state.current_char in 'rR'
        if is_raw:
            state.advance()
        
        quote = state.current_char
        string = quote
        state.advance()
        
        while state.current_char and (state.current_char != quote or string[-1] == '\\'):
            if state.current_char is None:
                raise LexerError("Unterminated string", start_pos.line, start_pos.column, state.get_context())
            string += state.current_char
            state.advance()
        
        if state.current_char == quote:
            string += quote
            state.advance()
        else:
            raise LexerError("Unterminated string", start_pos.line, start_pos.column, state.get_context())

        # Process the string value
        try:
            if is_raw:
                value = string[2:-1]
            else:
                value = string[1:-1].encode('utf-8').decode('unicode_escape')
            self._add_token(state, TokenType.STRING, value, start_pos, string)
        except UnicodeError as e:
            raise LexerError(f"Invalid string escape sequence: {e}", 
                           start_pos.line, 
                           start_pos.column,
                           state.get_context())

    def _handle_bytes(self, state: LexerState, start_pos: Position) -> None:
        bytes_str = ''
        while state.current_char and len(bytes_str) < 2:
            bytes_str += state.current_char
            state.advance()
        
        quote = state.current_char
        if quote not in '"\'':
            raise LexerError("Invalid bytes literal", start_pos.line, start_pos.column, state.get_context())
        
        bytes_str += quote
        state.advance()
        
        while state.current_char and (state.current_char != quote or bytes_str[-1] == '\\'):
            if state.current_char is None:
                raise LexerError("Unterminated bytes literal", 
                               start_pos.line, 
                               start_pos.column,
                               state.get_context())
            bytes_str += state.current_char
            state.advance()
        
        if state.current_char == quote:
            bytes_str += quote
            state.advance()
            try:
                value = eval(bytes_str)  # Safe for bytes literals
                self._add_token(state, TokenType.BYTES, value, start_pos, bytes_str)
            except SyntaxError:
                raise LexerError(f"Invalid bytes literal: {bytes_str}", 
                               start_pos.line, 
                               start_pos.column,
                               state.get_context())
        else:
            raise LexerError("Unterminated bytes literal", 
                           start_pos.line, 
                           start_pos.column,
                           state.get_context())

    def _handle_identifier(self, state: LexerState, start_pos: Position) -> None:
        identifier = ''
        while state.current_char and (state.current_char.isalnum() or state.current_char == '_'):
            identifier += state.current_char
            state.advance()

        if identifier in self.keywords:
            token_type = self.keywords[identifier]
            value = True if identifier == 'True' else False if identifier == 'False' else None
            self._add_token(state, token_type, value, start_pos, identifier)
        else:
            self._add_token(state, TokenType.IDENTIFIER, identifier, start_pos, identifier)

    def _handle_operator_or_delimiter(self, state: LexerState, start_pos: Position) -> None:
        if state.current_char in '([{':
            self._handle_opening_delimiter(state, start_pos)
        elif state.current_char in ')]}':
            self._handle_closing_delimiter(state, start_pos)
        elif state.current_char == '=' and state.peek() == '=':
            # Handle equality operator
            self._add_token(state, TokenType.EQUALS, '==', start_pos, '==')
            state.advance()
            state.advance()
        elif state.current_char == '=':
            # Handle assignment
            self._add_token(state, TokenType.ASSIGN, '=', start_pos, '=')
            state.advance()
        else:
            self._handle_operator(state, start_pos)

    def _handle_expression(self, state: LexerState, start_pos: Position) -> None:
        """Handle complex expressions with nested parentheses, operators, and control flow"""
        nesting_level = 0
        expression = ''
        
        while state.current_char:
            # Handle line continuation
            if state.current_char == '\\' and state.peek() == '\n':
                state.advance()  # Skip backslash
                state.advance()  # Skip newline
                while state.current_char and state.current_char.isspace():
                    state.advance()
                continue
                
            # Track nesting level for parentheses
            if state.current_char == '(':
                nesting_level += 1
                expression += state.current_char
            elif state.current_char == ')':
                nesting_level -= 1
                if nesting_level < 0:
                    break
                expression += state.current_char
            # Handle statement terminators
            elif nesting_level == 0 and state.current_char in (':', ';', '\n'):
                break
            else:
                expression += state.current_char
                
            state.advance()
            
            # Break if we've completed a top-level expression
            if nesting_level == 0 and state.current_char and (
                state.current_char in (':', ';', '\n') or 
                (state.current_char.isspace() and state.peek() in (':', ';', '\n'))
            ):
                break
                    
        # Tokenize the expression contents if we have any
        if expression:
            self._tokenize_expression_contents(state, expression, start_pos)

    def _tokenize_expression_contents(self, state: LexerState, expression: str, start_pos: Position) -> None:
        """Tokenize the contents of a complex expression with improved operator handling"""
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Handle numbers (including scientific notation)
            if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] in '.eE+-'):
                    if expression[i] in 'eE':
                        # Handle scientific notation
                        num_str += expression[i]
                        i += 1
                        if i < len(expression) and expression[i] in '+-':
                            num_str += expression[i]
                        else:
                            i -= 1
                    else:
                        num_str += expression[i]
                    i += 1
                i -= 1  # Back up one to account for the outer loop increment
                
                try:
                    if '.' in num_str or 'e' in num_str.lower():
                        value = float(num_str)
                        self._add_token(state, TokenType.FLOAT, value, start_pos, num_str)
                    else:
                        value = int(num_str)
                        self._add_token(state, TokenType.INTEGER, value, start_pos, num_str)
                except ValueError:
                    raise LexerError(f"Invalid number: {num_str}", 
                                start_pos.line, 
                                start_pos.column,
                                state.get_context())
            
            # Handle identifiers and keywords
            elif char.isalpha() or char == '_':
                identifier = ''
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                    identifier += expression[i]
                    i += 1
                i -= 1  # Back up one
                
                if identifier in self.keywords:
                    token_type = self.keywords[identifier]
                    value = True if identifier == 'True' else False if identifier == 'False' else None
                    self._add_token(state, token_type, value, start_pos, identifier)
                else:
                    self._add_token(state, TokenType.IDENTIFIER, identifier, start_pos, identifier)
            
            # Handle operators with precedence
            elif char in '+-*/%<>!=':
                # Try to match two-character operators first
                if i + 1 < len(expression):
                    two_char = char + expression[i + 1]
                    if two_char in self.operators:
                        self._add_token(state, self.operators[two_char], two_char, start_pos, two_char)
                        i += 1
                    elif char in self.operators:
                        self._add_token(state, self.operators[char], char, start_pos, char)
                else:
                    if char in self.operators:
                        self._add_token(state, self.operators[char], char, start_pos, char)
            
            # Handle parentheses for both grouping and tuples
            elif char == '(':
                self._add_token(state, TokenType.TUPLE_START, '(', start_pos, '(')
                state.nesting_levels['('] += 1
            elif char == ')':
                self._add_token(state, TokenType.TUPLE_END, ')', start_pos, ')')
                state.nesting_levels['('] -= 1
            
            # Handle string literals
            elif char in '"\'':
                self._handle_string_in_expression(state, start_pos, expression[i:])
                i = state.position.index  # Update position after handling string
                continue
            
            # Skip whitespace
            elif char.isspace():
                pass
            
            else:
                raise LexerError(f"Invalid character in expression: {char}", 
                            start_pos.line, 
                            start_pos.column,
                            state.get_context())
            
            i += 1

    def _handle_string_in_expression(self, state: LexerState, start_pos: Position, remaining: str) -> None:
        """Handle string literals within expressions"""
        quote = remaining[0]
        string = quote
        i = 1
        
        while i < len(remaining) and (remaining[i] != quote or remaining[i-1] == '\\'):
            string += remaining[i]
            i += 1
            
        if i < len(remaining) and remaining[i] == quote:
            string += quote
            value = string[1:-1].encode('utf-8').decode('unicode_escape')
            self._add_token(state, TokenType.STRING, value, start_pos, string)
            # Update state position
            for _ in range(len(string)):
                state.advance()
        else:
            raise LexerError("Unterminated string in expression",
                            start_pos.line,
                            start_pos.column,
                            state.get_context())

    def _handle_opening_delimiter(self, state: LexerState, start_pos: Position) -> None:
        delimiter = state.current_char
        state.nesting_levels[delimiter] += 1
        
        token_type = {
            '(': TokenType.TUPLE_START,
            '[': TokenType.LIST_START,
            '{': TokenType.DICT_START
        }[delimiter]
        
        # Check for set literal
        if delimiter == '{' and self._is_set_literal(state):
            token_type = TokenType.SET_START
            
        self._add_token(state, token_type, delimiter, start_pos, delimiter)
        state.advance()

    def _handle_closing_delimiter(self, state: LexerState, start_pos: Position) -> None:
        delimiter = state.current_char
        matching_open = {')': '(', ']': '[', '}': '{'}[delimiter]
        
        if state.nesting_levels[matching_open] == 0:
            raise LexerError(f"Unmatched closing delimiter: {delimiter}", 
                           start_pos.line, 
                           start_pos.column,
                           state.get_context())
                           
        state.nesting_levels[matching_open] -= 1
        
        token_type = {
            ')': TokenType.TUPLE_END,
            ']': TokenType.LIST_END,
            '}': TokenType.DICT_END if not self._is_set_literal(state) else TokenType.SET_END
        }[delimiter]
        
        self._add_token(state, token_type, delimiter, start_pos, delimiter)
        state.advance()

    def _handle_operator(self, state: LexerState, start_pos: Position) -> None:
        # Try to match two-character operators first
        two_char = state.current_char + (state.peek() or '')
        if two_char in self.operators:
            token_type = self.operators[two_char]
            self._add_token(state, token_type, two_char, start_pos, two_char)
            state.advance()
            state.advance()
            return

        # Handle single-character operators
        if state.current_char in self.operators:
            token_type = self.operators[state.current_char]
            self._add_token(state, token_type, state.current_char, start_pos, state.current_char)
            state.advance()
            return

        # Handle special characters
        if state.current_char in ',:':
            token_type = {
                ',': TokenType.COMMA,
                ':': TokenType.COLON
            }[state.current_char]
            self._add_token(state, token_type, state.current_char, start_pos, state.current_char)
            state.advance()
            return

        raise LexerError(f"Invalid character: {state.current_char}", 
                        start_pos.line, 
                        start_pos.column,
                        state.get_context())

    def _is_set_literal(self, state: LexerState) -> bool:
        """Determine if a curly brace represents a set literal rather than a dict."""
        # Look ahead for a colon to distinguish between set and dict
        pos = state.position.index
        nesting = 0
        while pos < len(state.source):
            char = state.source[pos]
            if char == '{':
                nesting += 1
            elif char == '}':
                nesting -= 1
                if nesting < 0:
                    return True  # No colon found before closing brace
            elif char == ':' and nesting == 0:
                return False  # Found colon at same nesting level
            pos += 1
        return True

    def _add_token(self, state: LexerState, token_type: TokenType, 
                  value: Any, start_pos: Position, raw: str) -> None:
        end_pos = state.position.copy()
        context = state.get_context()
        token = Token(token_type, value, start_pos, end_pos, raw, context)
        state.tokens.append(token)

    def _validate_final_state(self, state: LexerState) -> None:
        """Validate the final state of the lexer."""
        for char, level in state.nesting_levels.items():
            if level > 0:
                raise LexerError(f"Unclosed delimiter: {char}",
                               state.position.line,
                               state.position.column,
                               state.get_context())

        # Check for any other unfinished constructs
        if state.indentation_stack != [0]:
            raise LexerError("Inconsistent indentation at end of file",
                           state.position.line,
                           state.position.column,
                           state.get_context())
        
def lexer(source_code: str) -> list:
    """
    Tokenize Python source code into a list of token dictionaries.
    
    Args:
        source_code (str): Source code to tokenize
        
    Returns:
        list: List of token dictionaries with type, value and position
    """
    # Initialize the complex lexer
    complex_lexer = ComplexLexer()
    
    # Get raw tokens
    raw_tokens = complex_lexer.tokenize(source_code)
    
    # Convert to expected format
    formatted_tokens = []
    for token in raw_tokens:
        formatted_token = {
            'type': token.type.value,  # Convert enum to string
            'value': token.value,
            'position': token.position,  
        }
        formatted_tokens.append(formatted_token)
        
    return formatted_tokens