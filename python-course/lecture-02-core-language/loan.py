"""Loan calculator: monthly payment and the first year of the repayment schedule."""


def monthly_payment(principal, annual_rate, years):
    """Fixed monthly payment for a loan (standard amortisation formula)."""
    r = annual_rate / 100 / 12          # monthly interest rate
    n = years * 12                      # number of payments
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def schedule(principal, annual_rate, years, show_months=12):
    payment = monthly_payment(principal, annual_rate, years)
    balance = principal
    print(f"{'month':>5} {'interest':>12} {'principal':>12} {'balance':>14}")
    for month in range(1, show_months + 1):
        interest = balance * annual_rate / 100 / 12
        paid_off = payment - interest
        balance -= paid_off
        print(f"{month:>5} {interest:>12,.2f} {paid_off:>12,.2f} {balance:>14,.2f}")
    return payment


def main():
    principal = float(input("Loan amount: "))
    annual_rate = float(input("Yearly interest rate (%): "))
    years = int(input("Years: "))

    payment = schedule(principal, annual_rate, years)
    total = payment * years * 12
    print(f"\nMonthly payment: {payment:,.2f}")
    print(f"Total paid:      {total:,.2f}")
    print(f"Total interest:  {total - principal:,.2f}  ({(total - principal) / principal:.1%} of the loan)")


if __name__ == "__main__":
    main()
