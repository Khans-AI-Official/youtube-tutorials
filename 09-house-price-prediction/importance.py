import joblib
import pandas as pd

model = joblib.load("house_model.joblib")
forest = model[-1]

names = model.feature_names_in_
importance = pd.Series(forest.feature_importances_, index=names)
print(importance.sort_values(ascending=False).round(3))
