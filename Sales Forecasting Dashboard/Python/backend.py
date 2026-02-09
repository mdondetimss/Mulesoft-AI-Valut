import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# 1. Load and preprocess data
def load_data(filepath):
    data = pd.read_csv(filepath)
    data["Order Date"] = pd.to_datetime(data["Order Date"], format="%d/%m/%Y") # Converting Order Date From string to date.
    return data


def aggregate_sales(data):
    sales_by_date = data.groupby("Order Date")["Sales"].sum().reset_index() #Grouping the data by Order Date.
    return sales_by_date


# 2. Feature Engineering
def create_lagged_data(data, lag=5):
    lagged_data = data.copy() # Copying data to prevent coruption for main file.
    for i in range(1, lag + 1):
        lagged_data[f"lag_{i}"] = lagged_data["Sales"].shift(i)
    return lagged_data.dropna() # Dropinng values that have NA in there fields.


# 3. Train Model
def train_model(sales_data, lag=5):

    sales_with_lags = create_lagged_data(sales_data, lag)

    X = sales_with_lags.drop(columns=["Order Date", "Sales"])
    y = sales_with_lags["Sales"]
    # Spliting the train to test ratio as 10:2.
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5
    )

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    return {
        "model": model,
        "x_test": x_test,
        "y_test": y_test,
        "predictions": predictions,
        "rmse": rmse
    }


# 4. Full Pipeline
# Organizing all the functions into the flow
def run_pipeline(filepath, lag=5):
    data = load_data(filepath)
    aggregated = aggregate_sales(data)
    results = train_model(aggregated, lag)
    return aggregated, results
