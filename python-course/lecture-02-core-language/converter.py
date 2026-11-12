"""Unit converter: read a value and a conversion, check the input, print a table."""

# key: (from unit, to unit, multiply by, then add)
CONVERSIONS = {
    "km-mi": ("kilometres", "miles", 0.621371, 0),
    "kg-lb": ("kilograms", "pounds", 2.204623, 0),
    "c-f": ("Celsius", "Fahrenheit", 1.8, 32),
}


def ask_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        text = input(prompt)
        try:
            return float(text)
        except ValueError:
            print(f"  '{text}' is not a number, try again")


def main():
    print("Conversions:", ", ".join(CONVERSIONS))
    while True:
        key = input("Which conversion? ").strip().lower()
        if key in CONVERSIONS:
            break
        print(f"  unknown conversion '{key}'")

    source, target, factor, offset = CONVERSIONS[key]
    value = ask_number(f"How many {source}? ")

    print(f"\n{source:>12} | {target:<12}")
    print("-" * 27)
    for step in range(1, 6):
        v = value * step
        print(f"{v:>12,.2f} | {v * factor + offset:<12,.2f}")


if __name__ == "__main__":
    main()
