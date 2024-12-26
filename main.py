
from lib.syntax import syntax




def greet(name):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    greet(syntax.get("name", "No Name Defined"))
