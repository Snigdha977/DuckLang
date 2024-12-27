# Importing regular expression module
import re
# Importing syntax definitions
from lib.syntax import syntax
# Importing token types dictionary
from src.lexer.token_types import TOKEN_TYPES

# Retrieve the print command syntax from the syntax dictionary
print_command = syntax.get("PRINT_COMMAND", "No Name Defined")
# Retrieve the variable declaration command syntax from the syntax dictionary
var_declare_command = syntax.get("VARIABLE_DECLARE", "No Name Defined")

def identify_literal_type(value_str):
    """Identify the type of a literal value."""
    value_str = value_str.strip()

    # Check for None/null literals
    if value_str.lower() in ('none', 'null'):
        return TOKEN_TYPES["NONE_LITERAL"], None
        
    # Check for boolean literals (true/false)
    if value_str.lower() in ('true', 'false'):
        return TOKEN_TYPES["BOOLEAN_LITERAL"], value_str.lower() == 'true'
        
    # Check for float literals (including scientific notation)
    try:
        if '.' in value_str or 'e' in value_str.lower():
            float_val = float(value_str)
            return TOKEN_TYPES["FLOAT_LITERAL"], float_val
    except ValueError:
        pass
        
    # Check for integer literals (supports different bases: hex, binary, octal)
    try:
        if value_str.startswith('0x'):
            int_val = int(value_str[2:], 16)
        elif value_str.startswith('0b'):
            int_val = int(value_str[2:], 2)
        elif value_str.startswith('0o'):
            int_val = int(value_str[2:], 8)
        else:
            int_val = int(value_str)
        return TOKEN_TYPES["INTEGER_LITERAL"], int_val
    except ValueError:
        pass
    
    # If it’s a string literal, it should be enclosed in quotes
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return TOKEN_TYPES["STRING_LITERAL"], value_str[1:-1]
        
    # Return as unknown if no match is found
    return TOKEN_TYPES["UNKNOWN"], value_str

def lexer(source_code):
    """Function for lexical analysis to tokenize the source code."""
    tokens = []
    position = 0  # Initialize the position pointer to track character position

    while position < len(source_code):
        # Skip whitespace
        match = re.match(r'\s+', source_code[position:])
        if match:
            position += len(match.group(0))  # Move the position forward
            continue

        # Match print statements (e.g., print("Hello World"))
        match = re.match(rf'\b{re.escape(print_command)}\(([^)]+)\)', source_code[position:])
        if match:
            # Create a print token with its position and content
            print_token = {
                'type': TOKEN_TYPES["PRINT_COMMAND"],
                'value': match.group(0),
                'position': position,
                'raw': match.group(0)
            }
            tokens.append(print_token)
            
            # Analyze the content inside print statement (literal or expression)
            content = match.group(1).strip()
            literal_type, literal_value = identify_literal_type(content)
            
            # Create a value token (literal) with the identified type
            value_token = {
                'type': literal_type,
                'value': literal_value,
                'position': position + len(print_command) + 1,  # Position after print command
                'raw': content
            }
            tokens.append(value_token)
            
            position += len(match.group(0))  # Move position to the end of the matched print statement
            continue

        # Match variable declarations (e.g., let x = 5)
        match = re.match(
            rf'\b{re.escape(var_declare_command)}\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^;\n]+)',
            source_code[position:]
        )
        if match:
            # Create a token for the variable declaration command (e.g., let)
            var_decl_token = {
                'type': TOKEN_TYPES["VARIABLE_DECLARE"],
                'value': var_declare_command,
                'position': position,
                'raw': var_declare_command
            }
            tokens.append(var_decl_token)

            # Create a token for the variable name (identifier)
            identifier_token = {
                'type': TOKEN_TYPES["IDENTIFIER"],
                'value': match.group(1),
                'position': position + len(var_declare_command) + 1,  # Position after 'let'
                'raw': match.group(1)
            }
            tokens.append(identifier_token)

            # Create a token for the equals sign in the variable declaration
            equals_token = {
                'type': TOKEN_TYPES["EQUALS"],
                'value': '=',
                'position': position + len(var_declare_command) + len(match.group(1)) + 1,  # Position after variable name
                'raw': '='
            }
            tokens.append(equals_token)

            # Identify the type of the value assigned to the variable
            value_str = match.group(2).strip()
            literal_type, literal_value = identify_literal_type(value_str)
            
            # Create a token for the assigned value with the identified type
            value_token = {
                'type': literal_type,
                'value': literal_value,
                'position': position + len(match.group(0)) - len(value_str),
                'raw': value_str
            }
            tokens.append(value_token)
            
            position += len(match.group(0))  # Move position to the end of the matched variable declaration
            continue

        # If no match is found for any known patterns, move to the next character
        position += 1

    return tokens  # Return the list of tokenized results
