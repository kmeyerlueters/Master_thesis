import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load the merged dataset that contains both original and modified arguments
merged_df = pd.read_csv('../_merged_og_mod_ratings.csv', delimiter=';')

# Convert 'Modified_Rating' to numeric, setting invalid entries (e.g., 'No Match') to NaN
merged_df['Modified_Rating'] = pd.to_numeric(merged_df['Modified_Rating'], errors='coerce')

# Drop rows where 'Modified_Rating' is NaN (i.e., no matching modified argument found)
merged_df = merged_df.dropna(subset=['Modified_Rating'])

# Calculate the residuals between the model ratings and the original human ratings (WA)
merged_df['residuals'] = merged_df['Modified_Rating'] - merged_df['Original_WA_Rating']

# Calculate the absolute differences between the original human ratings (WA) and the language model ratings
merged_df['absolute_difference'] = np.abs(merged_df['residuals'])

# Calculate overall statistics for the absolute differences
overall_mae = mean_absolute_error(merged_df['Original_WA_Rating'], merged_df['Modified_Rating'])
overall_mse = mean_squared_error(merged_df['Original_WA_Rating'], merged_df['Modified_Rating'])
mean_diff = merged_df['absolute_difference'].mean()
std_diff = merged_df['absolute_difference'].std()
min_diff = merged_df['absolute_difference'].min()
max_diff = merged_df['absolute_difference'].max()

# Print overall statistics
print(f"Overall Mean Absolute Error (MAE): {overall_mae}")
print(f"Overall Mean Squared Error (MSE): {overall_mse}")
print(f"Mean of Absolute Differences: {mean_diff}")
print(f"Standard Deviation of Absolute Differences: {std_diff}")
print(f"Minimum Absolute Difference: {min_diff}")
print(f"Maximum Absolute Difference: {max_diff}")

# Print summary of residuals
print("Summary of Residuals:")
print(merged_df['residuals'].describe())

# Optionally: Save the dataset with absolute differences and residuals
merged_df.to_csv('output_filev', sep=';', index=False)

print("Merged dataset with overall differences and residuals saved to 'Yi-Chat-merged_overall_differences_with_residuals.csv'.")
