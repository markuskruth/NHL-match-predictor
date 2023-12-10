import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.neural_network import MLPRegressor

import data_setup

def get_X_and_y():
    df = data_setup.process_data("all_teams.csv")

    X_raw = df.drop(columns = ["prediction"])
    y = df["prediction"]

    # one-hot encoding
    X = pd.get_dummies(X_raw, dtype=int)

    return X,X_raw,y

def LR_model(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=2)

    clf = LinearRegression()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    mse_score = mean_squared_error(y_pred, y_test)
    print("MSE:", mse_score)

    return clf

def NN_model(X,y, layers):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=2)
    neurons = 15

    hidden_layer_sizes = tuple([neurons]*layers)

    mlp_regr = MLPRegressor(random_state=42, max_iter=1000, hidden_layer_sizes=hidden_layer_sizes)
    mlp_regr.fit(X_train, y_train)

    y_pred = mlp_regr.predict(X_test)
    mse_score = mean_squared_error(y_pred, y_test)
    print(f"MSE for layers={layers}:", mse_score)

    return mlp_regr
    


def predict(clf, X_raw, pred_data):
    #data_setup.print_teams()
    predict_data = pd.DataFrame({"playerTeam": [pred_data[0]], "opposingTeam": [pred_data[1]], "home_or_away": [pred_data[2]]})
    predict_data_encoded = pd.get_dummies(predict_data, columns=X_raw.columns, dtype=int)

    # Add missing columns with zeros
    for col in X.columns:
        if col not in predict_data_encoded.columns:
            predict_data_encoded[col] = 0

    # reorder columns to the right order
    predict_data_encoded = predict_data_encoded[X.columns]

    # Make predictions for the new data
    prediction = clf.predict(predict_data_encoded)

    return prediction
    

if __name__ == "__main__":
    X,X_raw,y = get_X_and_y()
    #clf = LR_model(X,y)
    clf = NN_model(X,y, 2)
    data_setup.print_teams()
    while True:
        home = input("Home: ")
        away = input("Away: ")
        pred_data = [home, away, "HOME"]
        prediction = predict(clf, X_raw, pred_data)

        print("Prediction:", prediction, "\n")