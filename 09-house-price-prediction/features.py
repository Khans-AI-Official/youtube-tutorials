import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

df = pd.read_csv("housing.csv")
df["rooms_per_household"] = df["total_rooms"] / df["households"]
df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
df["people_per_household"] = df["population"] / df["households"]

X = pd.get_dummies(df.drop(columns="median_house_value"))
y = df["median_house_value"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

forest = make_pipeline(
    SimpleImputer(strategy="median"),
    RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1),
)
scores = cross_val_score(
    forest, X_train, y_train, cv=5, scoring="neg_mean_absolute_error"
)
print(f"random forest + 3 new features: ${-scores.mean():,.0f} off")
