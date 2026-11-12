"""Loan calculator, first attempt."""

principal = input("Loan amount: ")
annual_rate = input("Yearly interest rate (%): ")
years = input("Years: ")

monthly_rate = annual_rate / 100 / 12
months = years * 12
payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
print("Monthly payment:", payment)
