"""Functions: arguments, defaults, *args, **kwargs, return values."""


def area(width, height=1):
    return width * height


def total(*amounts):
    """Any number of positional arguments arrive as a tuple."""
    return sum(amounts)


def describe(name, **details):
    """Any number of keyword arguments arrive as a dict."""
    parts = [f"{key}={value}" for key, value in details.items()]
    return f"{name}: " + ", ".join(parts)


print(area(3))                # height takes its default
print(area(3, 4))             # positional
print(area(height=4, width=3))  # by keyword, any order
print(total(500, 750, 300))
print(describe("loan", amount=5_000_000, rate=12, years=20))
