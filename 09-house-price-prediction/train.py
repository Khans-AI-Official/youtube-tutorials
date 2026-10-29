import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("housing.csv")
X = df.drop(columns="median_house_value")
X = pd.get_dummies(X)
y = df["median_house_value"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

def average_error(model):
    scores = cross_val_score(
        model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error"
    )
    return -scores.mean()

print(f"always guess the average: ${average_error(DummyRegressor()):,.0f} off")

linear = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
print(f"linear regression:        ${average_error(linear):,.0f} off")

forest = make_pipeline(
    SimpleImputer(strategy="median"),
    RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1),
)
print(f"random forest:            ${average_error(forest):,.0f} off")

forest.fit(X_train, y_train)
test_error = mean_absolute_error(y_test, forest.predict(X_test))
print(f"random forest on the test set: ${test_error:,.0f} off")

joblib.dump(forest, "house_model.joblib")
print("saved house_model.joblib")
