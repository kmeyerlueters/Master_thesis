# Comparison of human vs. LLM annotations for each identity version

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Function to process each model and return the grouped difference DataFrame
def process_model(file_path, original_df):
    # Load the modified dataset
    modified_df = pd.read_csv(file_path, delimiter=';')

    # Convert 'average_extracted_number' to numeric, forcing errors to NaN
    modified_df['average_extracted_number'] = pd.to_numeric(modified_df['average_extracted_number'], errors='coerce')

    # Normalize the new ratings (if not already normalized), ignoring NaN values
    modified_df['normalized_rating'] = modified_df['average_extracted_number'] / 5.0

    # Drop rows where 'normalized_rating' is NaN (this will remove invalid entries)
    modified_df = modified_df.dropna(subset=['normalized_rating'])

    # Ensure 'Version' column is a string
    modified_df['Version'] = modified_df['Version'].astype(str)

    # Merge the datasets on 'ID'
    merged_df = pd.merge(modified_df, original_df[['ID', 'WA']], on='ID')

    # Calculate the difference between the original and new ratings
    merged_df['rating_difference'] = merged_df['normalized_rating'] - merged_df['WA']

    # Group the differences by the 'Version' column
    grouped_diff = merged_df.groupby('Version')['rating_difference'].agg(['mean', 'std', 'min', 'max', 'count'])

    # Calculate Mean Absolute Error (MAE) and Mean Squared Error (MSE) for each group
    grouped_diff['mae'] = merged_df.groupby('Version').apply(lambda x: mean_absolute_error(x['WA'], x['normalized_rating']))
    grouped_diff['mse'] = merged_df.groupby('Version').apply(lambda x: mean_squared_error(x['WA'], x['normalized_rating']))

    return grouped_diff

# Load the original dataset (shared across all models)
original_df = pd.read_csv('/input', delimiter=';')

# File paths for each model
model_files = {
    'Llama 3': 'input_file',
    'Phi-3': 'input_file',
    'Yi-Chat': 'input_file'
}

# Store results for each model
model_results = {}

# Process each model
for model_name, file_path in model_files.items():
    model_results[model_name] = process_model(file_path, original_df)

# Combine all model results into a single DataFrame for comparison
combined_results = pd.concat(model_results, names=['Model', 'Version'])

# Sort the combined results by the 'mae' of one specific model (e.g., 'Phi')
sorted_combined_results = combined_results.loc['Phi-3'].sort_values(by='mae', ascending=False)

# Get the sorted version order
sorted_versions = sorted_combined_results.index.tolist()

# Reorder the rows of the combined results based on the sorted version order
reordered_combined_results = combined_results.loc[(slice(None), sorted_versions), :]

# Define custom colors for each model
colors = {
    'Llama 3': '#FFA544',
    'Phi-3': '#4EB8E9',
    'Yi-Chat': '#A5E161'
}

# Define a mapping from original version names to new display names
version_name_map = {
    'Black Male': 'Black man',
    'Black Female': 'Black woman',
    'White Male': 'White man',
    'White Female': 'White woman',
    'Black Trans Woman': 'Black trans woman',
    'Black Trans Man': 'Black trans man',
    'Black Cis Woman': 'Black cis woman',
    'Black Cis Man': 'Black cis man',
    'White Trans Woman': 'White trans woman',
    'White Trans Man': 'White trans man',
    'White Cis Woman': 'White cis woman',
    'White Cis Man': 'White cis man',
    'Neutral': 'Neutral',
    'Person of color': 'Person of color',
    'Cis man': 'Cis man',
    'Cis woman': 'Cis woman',
    'Cis person': 'Cis person',
    'Trans woman': 'Trans woman',
    'Trans man': 'Trans man',
    'Trans person': 'Trans person',
    'Female': 'Woman',
    'Male': 'Man',
    'Black person': 'Black person',
    'White person': 'White person'
}

# Visualization - Compare MAE for each version across models
fig, ax = plt.subplots(figsize=(12, 8))

for model_name in model_files.keys():
    ax.plot(reordered_combined_results.loc[model_name].index.get_level_values(0).map(lambda x: version_name_map.get(str(x), str(x))), 
             reordered_combined_results.loc[model_name]['mae'], 
             label=model_name, color=colors[model_name])

# Adding title and axis labels with padding
# ax.set_title('MAE Comparison Across Models and Versions', pad=20)  # Adjust the padding for the title
ax.set_xlabel('Version', labelpad=20)  # Adjust the padding for x-axis label
ax.set_ylabel('MAE', labelpad=20)  # Adjust the padding for y-axis label
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Remove the box by hiding the top, right, and left spines
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
# ax.spines["left"].set_visible(False)

# Only show ticks on the bottom spine
ax.yaxis.set_ticks_position("none")
ax.xaxis.set_ticks_position("bottom")

ax.legend(frameon=True, fontsize=14)

# Adjust bottom margin to make room for long x-axis labels
plt.subplots_adjust(bottom=0.25)

# Tight layout to prevent overlap
plt.tight_layout()

# Adding guidelines (gridlines)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Adjust the linestyle and width for clearer gridlines
plt.grid(axis='x', color='gray', linestyle='--', linewidth=0.5)
plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)

plt.savefig('output_path', dpi=300)



