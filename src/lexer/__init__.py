"""Module providing RE"""
import re
"""Module providing Syntax Dictionary."""
from lib.syntax import syntax
"""Module providing Token_Type Dictionary."""
from src.lexer.token_types import TOKEN_TYPES


print_command = syntax.get("PRINT_COMMAND", "No Name Defined")


def lexer(source_code):
    """Function For Print_Statement."""
    tokens = []
    quack_pattern = rf'\b{re.escape(print_command)}\(([^)]+)\)' 
    matches = re.finditer(quack_pattern, source_code)

    for match in matches:
            print_token = {
                'type': TOKEN_TYPES["PRINT"],
                'value': match.group(0),  
                'position': match.start()
            }
            tokens.append(print_token)

            string_token = {
                'type': TOKEN_TYPES["STRING"],
                'value': match.group(1),  
                'position': match.start(1)
            }
            tokens.append(string_token)

    return tokens
