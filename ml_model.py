import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score

import data_setup

df = data_setup.process_data("all_teams.csv")

X_raw = df.drop(columns = ["prediction"])
y = df["prediction"]

# one-hot encoding
X = pd.get_dummies(X_raw, dtype=int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=2)

clf = LinearRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
mse_score = mean_squared_error(y_pred, y_test)
print("MSE:", mse_score)

data_setup.print_teams()
predict_data = pd.DataFrame({"playerTeam": ["BOS"], "opposingTeam": ["ANA"], "home_or_away": ["HOME"]})
predict_data_encoded = pd.get_dummies(predict_data, columns=X_raw.columns, dtype=int)

# Add missing columns with zeros
for col in X.columns:
    if col not in predict_data_encoded.columns:
        predict_data_encoded[col] = 0

# reorder columns to the right order
predict_data_encoded = predict_data_encoded[X.columns]

# Make predictions for the new data
predictions = clf.predict(predict_data_encoded)

print("Predictions for predict_data:", predictions)