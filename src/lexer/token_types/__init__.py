'''A comprehensive dictionary of token types for lexical analysis'''
TOKEN_TYPES = {
    # Custom tokens
    "PRINT_COMMAND": "PRINT_COMMAND",
    "VARIABLE_DECLARE": "VARIABLE_DECLARE",

    # Basic types
    "IDENTIFIER": "IDENTIFIER",
    "INTEGER": "INTEGER",
    "FLOAT": "FLOAT",
    "STRING": "STRING",
    "BYTES": "BYTES",
    "BOOLEAN": "BOOLEAN",
    "NONE": "NONE",

    # Collections
    "LIST_START": "LIST_START",
    "LIST_END": "LIST_END",
    "TUPLE_START": "TUPLE_START",
    "TUPLE_END": "TUPLE_END",
    "DICT_START": "DICT_START",
    "DICT_END": "DICT_END",
    "SET_START": "SET_START",
    "SET_END": "SET_END",

    # Operators
    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "MULTIPLY": "MULTIPLY",
    "DIVIDE": "DIVIDE",
    "FLOOR_DIVIDE": "FLOOR_DIVIDE",
    "POWER": "POWER",
    "MODULO": "MODULO",

    # Comparisons
    "EQUALS": "EQUALS",
    "NOT_EQUALS": "NOT_EQUALS",
    "LESS_THAN": "LESS_THAN",
    "GREATER_THAN": "GREATER_THAN",
    "LESS_EQUAL": "LESS_EQUAL",
    "GREATER_EQUAL": "GREATER_EQUAL",

    # Logical
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",
    "IN": "IN",
    "NOT_IN": "NOT_IN",
    "IS": "IS",
    "IS_NOT": "IS_NOT",

    # Comprehension
    "FOR": "FOR",
    "IF": "IF",
    "ELSE": "ELSE",

    # Other
    "COMMA": "COMMA",
    "DOT": "DOT",
    "COLON": "COLON",
    "ASSIGN": "ASSIGN",
    "ARROW": "ARROW",
    "LAMBDA": "LAMBDA",
    "WALRUS": "WALRUS",
}
