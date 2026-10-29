import joblib
import pandas as pd

model = joblib.load("house_model.joblib")

district = {
    "longitude": -118.3, "latitude": 34.1, "housing_median_age": 30,
    "total_rooms": 2000, "total_bedrooms": 400, "population": 1000,
    "households": 380, "ocean_proximity": "<1H OCEAN",
}

for income in [2.0, 4.0, 8.0]:
    new = pd.DataFrame([{**district, "median_income": income}])
    new = pd.get_dummies(new)
    new = new.reindex(columns=model.feature_names_in_, fill_value=0)
    price = model.predict(new)[0]
    print(f"median income {income:.1f} -> predicted value ${price:,.0f}")
