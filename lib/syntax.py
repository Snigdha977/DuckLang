from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv("NAME", "UNKNOWN")
print_command = os.getenv("PRINT_COMMAND", "UNKNOWN")


syntax = {
    "name": name,
    "PRINT_COMMAND": print_command,
}