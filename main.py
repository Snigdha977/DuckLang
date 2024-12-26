from dotenv import load_dotenv
import os


load_dotenv()
name = os.getenv("NAME", "UNKNOWN")  

def greet(name):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    greet(name)
