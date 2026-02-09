import pandas as pd
import matplotlib.pyplot as plt

# Load the training dataset from a CSV file into a pandas DataFrame
filepath = "train.csv"
data = pd.read_csv(filepath)
# print(data.head())

# Convert the 'Order Date' column from string format to pandas datetime
# This is required for proper time-series grouping and plotting
data["Order Date"] = pd.to_datetime(data["Order Date"], format="%d/%m/%Y")

# Aggregate total sales per day by grouping on 'Order Date'
# This collapses multiple orders on the same date into a single daily sales value
sales_by_date = data.groupby("Order Date")["Sales"].sum().reset_index()
# print(sales_by_date)

# Plot total sales over time to visualize the trend and variability
plt.figure(figsize=(16,9))
plt.plot(sales_by_date["Order Date"],sales_by_date["Sales"],label="Sales_Count",color="Green")
plt.title("Sales over time")
plt.xlabel("Dates")
plt.ylabel("Sales")
plt.grid(True)
plt.legend()
plt.show()

# Function to convert a time series into a supervised learning dataset
# by adding lagged versions of the target variable as features
def create_lagged_data(data, lag=1):
    lagged_data = data.copy()
    # Create lag_1, lag_2, ..., lag_n features using shifted Sales values
    for i in range(1, lag + 1):
        lagged_data[f"lag_{i}"] = lagged_data["Sales"].shift(i)
    return lagged_data

# Generate a dataset with 5 lag features (previous 5 sales values)
sales_with_lags = create_lagged_data(
    data[["Order Date", "Sales"]],
    lag=5
)
# print(sales_with_lags.head(10))

# Remove rows with NaN values caused by lagging
# These rows cannot be used for supervised learning
sales_with_lags = sales_with_lags.dropna()
# print(sales_with_lags.head(10))

# Separate input features (lagged sales) and target variable (current sales)
x = sales_with_lags.drop(columns=["Order Date", "Sales"])
y = sales_with_lags["Sales"]

# Split the dataset into training and testing sets
# shuffle=False preserves temporal order, which is mandatory for time series
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

import xgboost as xgb
import numpy as np

# Initialize the XGBoost regression model with standard hyperparameters
# This model learns a non-linear mapping from lagged sales to future sales
model_xgb = xgb.XGBRegressor(objective='reg:squarederror',n_estimators=100,learning_rate=0.1,max_depth=5)

# Train the model on historical lagged sales data
model_xgb.fit(x_train, y_train)

from sklearn.metrics import mean_squared_error

# Generate predictions for the test period
predictions_xgb = model_xgb.predict(x_test)

# Compute Root Mean Squared Error to evaluate forecast accuracy
rmse_xgb = np.sqrt(mean_squared_error(y_test, predictions_xgb))
print(f"RMSE: {rmse_xgb:.2f}")

# Plot actual vs predicted sales to visually assess model performance
plt.figure(figsize=(16, 9))
plt.plot(y_test.index, y_test, label='Actual Sales', color='red')
plt.plot(y_test.index, predictions_xgb, label='Predicted Sales', color='Blue')
plt.title('Sales Forecasting using XGBoost')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()