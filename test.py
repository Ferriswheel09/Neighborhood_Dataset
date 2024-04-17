from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelBinarizer
import numpy as np


# Sample data
prices = [100000, 150000, 200000]  # Sample prices
square_feet = [1000, 1500, 2000]    # Sample square feet
states = ["Ashburn, VA", "New York, NY", "Los Angeles, CA"]  # Sample states

# Initialize LabelBinarizer
label_binarizer = LabelBinarizer()

# Fit and transform the states
encoded_states = label_binarizer.fit_transform(states)

# Concatenate the features
X = np.concatenate([encoded_states, np.array(prices).reshape(-1, 1), np.array(square_feet).reshape(-1, 1)], axis=1)

# Target variable
y = np.array([200, 300, 400])  # Sample target values

# Initialize and fit the model
model = LinearRegression()
model.fit(X, y)

# Predict on new data
new_prices = [180000, 220000]
new_square_feet = [1200, 1800]
new_states = ["Ashburn, VA", "Los Angeles, CA"]
new_encoded_states = label_binarizer.transform(new_states)
new_X = np.concatenate([new_encoded_states, np.array(new_prices).reshape(-1, 1), np.array(new_square_feet).reshape(-1, 1)], axis=1)

predictions = model.predict(new_X)

print("Predictions:", predictions)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score

# Calculate predictions
predictions = model.predict(X)

# Calculate mean absolute error
mae = mean_absolute_error(y, predictions)

# Calculate mean squared error
mse = mean_squared_error(y, predictions)

# Calculate R-squared
r2 = r2_score(y, predictions)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("R-squared:", r2)