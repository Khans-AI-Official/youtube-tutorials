# 09 · House Price Prediction with Machine Learning in Python

Code for the Khan's AI video. Predicts the median house value of California districts (California Housing dataset, 1990 US census) with scikit-learn.

## Data

`housing.csv` (20,640 rows, 10 columns), the version from Aurélien Géron's *Hands-On Machine Learning* repository:
https://github.com/ageron/handson-ml2/tree/master/datasets/housing

Put `housing.csv` next to the scripts.

## Results from the run in the video

| Model | Average error (MAE) |
|---|---|
| Always guess the average (5-fold CV) | $91,379 |
| Linear regression (5-fold CV) | $49,989 |
| Random forest (5-fold CV) | $32,365 |
| Random forest + 3 ratio features (5-fold CV) | $33,131 (worse, so dropped) |
| **Random forest on the test set (4,128 districts)** | **$31,638** |

Below the $500,001 cap the test error is $29,721; for the 181 capped test districts it is $73,441.

## Run it

```bash
pip install -r requirements.txt
python explore.py      # shape, missing values, categories, price summary
python train.py        # baseline, linear regression, random forest, final test; saves house_model.joblib (~144 MB)
python features.py     # tries 3 ratio features with the same forest
python errors.py       # test error below vs at the price cap
python importance.py   # feature importances
python predict.py      # predictions for one district at three income levels
```

Results can differ slightly with other library versions.
