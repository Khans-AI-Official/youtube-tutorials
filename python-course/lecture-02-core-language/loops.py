"""Loops: for, while, break, continue, and else on a loop."""

# while: how many years until savings double at 12% a year?
balance, years = 1000.0, 0
while balance < 2000:
    balance *= 1.12
    years += 1
print(f"doubled after {years} years: {balance:,.2f}")

# continue: skip the entries we don't want
payments = [500, -20, 750, 0, 300]
total = 0
for p in payments:
    if p <= 0:
        continue
    total += p
print("total of positive payments:", total)

# break + else: the else runs only if the loop did NOT break
for n in [9, 15, 21, 27]:
    if n % 2 == 0:
        print("found an even number:", n)
        break
else:
    print("no even number in the list")
