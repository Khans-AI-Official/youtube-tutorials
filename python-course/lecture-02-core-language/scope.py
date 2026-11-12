"""Scope: Python looks names up Local, Enclosing, Global, Built-in (LEGB)."""
x = "global"


def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print("inner sees:", x)

    inner()
    print("outer sees:", x)


outer()
print("module sees:", x)
print("built-in len:", len("LEGB"))

counter = 0


def add_one():
    counter += 1    # assigning makes 'counter' local to this function


add_one()
