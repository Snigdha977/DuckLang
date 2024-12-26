"""Module providing Syntax Dictionary."""
from lib.syntax import syntax
"""Module providing Lexer Function"""
from src.lexer import lexer



source_code = 'quack("Hello World")'

def run_lexer(source_code):
    '''Call the lexer to tokenize the source code'''
    tokens = lexer(source_code)
    for token in tokens:
        print(f"Token Type: {token['type']}, Value: {token['value']}, Position: {token['position']}")

if __name__ == "__main__":
    run_lexer(source_code)
