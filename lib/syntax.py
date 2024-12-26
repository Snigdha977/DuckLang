from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv("NAME", "UNKNOWN")


syntax = {
    "name": name
}