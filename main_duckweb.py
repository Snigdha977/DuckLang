"""Module providing Syntax Dictionary."""
from lib.syntax import syntax
"""Module providing Lexer Function"""
from src.lexer import lexer



source_code = '''
quack("Hello World")
duck my_int = 42
duck my_float = 3.14
quck(my_int+my_float)
duck my_bool = True
'''

def run_lexer(source_code):
    '''Call the lexer to tokenize the source code'''
    tokens = lexer(source_code)
    
    # Print header
    print(f"{'Token Type':<25} {'Value':<30} {'Position'}")
    print("="*80)  # Separator line
    
    # Print each token in a well-formatted way
    for token in tokens:
        token_type = token['type']
        value = token['value']
        position = token['position']
        
        # Print token info with proper formatting
        print(f"{token_type:<25} {str(value):<30} {position}")
    
if __name__ == "__main__":
    run_lexer(source_code)
