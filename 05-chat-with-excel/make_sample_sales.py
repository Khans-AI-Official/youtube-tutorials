"""Creates sales.xlsx, a small sample file to try excel_chat.py with."""
import random

import pandas as pd

random.seed(7)
cities = ["Lahore", "Karachi", "Peshawar", "Islamabad", "Quetta"]
products = ["Rice 5kg", "Cooking oil 1L", "Sugar 1kg", "Tea 500g", "Flour 10kg"]
months = ["January", "February", "March"]
rows = []
for m in months:
    for _ in range(80):
        city, product = random.choice(cities), random.choice(products)
        qty = random.randint(5, 60)
        price = {"Rice 5kg": 1600, "Cooking oil 1L": 650, "Sugar 1kg": 160,
                 "Tea 500g": 950, "Flour 10kg": 1350}[product]
        rows.append({"month": m, "city": city, "product": product,
                     "quantity": qty, "revenue": qty * price})
pd.DataFrame(rows).to_excel("sales.xlsx", index=False)
print("Saved sales.xlsx with", len(rows), "rows")
