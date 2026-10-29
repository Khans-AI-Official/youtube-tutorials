import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("housing.csv")
X = pd.get_dummies(df.drop(columns="median_house_value"))
y = df["median_house_value"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

model = joblib.load("house_model.joblib")
errors = abs(model.predict(X_test) - y_test)
capped = y_test == 500001

below, at_cap = errors[~capped], errors[capped]
print(f"below the cap: ${below.mean():,.0f} off  ({len(below)} districts)")
print(f"at the cap:    ${at_cap.mean():,.0f} off  ({len(at_cap)} districts)")
