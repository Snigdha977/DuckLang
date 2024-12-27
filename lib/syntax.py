from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv("NAME", "UNKNOWN")
print_command = os.getenv("PRINT_COMMAND", "UNKNOWN")
var_command = os.getenv("VARIABLE_DECLARE", "UNKNOWN")


syntax = {
    "name": name,
    "PRINT_COMMAND": print_command,
    "VARIABLE_DECLARE": var_command,
}

