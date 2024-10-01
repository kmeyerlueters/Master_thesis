import pandas as pd

# Load the CSV file
file_path = 'input_file'
data = pd.read_csv(file_path, delimiter=';')

# Filter out rows where the average_extracted_number is 0
zero_ratings = data[data['average_extracted_number'] == 0]

# Group by Version and count the number of 0 ratings per Version
zero_ratings_count = zero_ratings.groupby('Version').size()

# Sort the results to show the Versions with the most 0 ratings first
sorted_zero_ratings = zero_ratings_count.sort_values(ascending=False)

# Print the results
print("Groups with the Most Ratings of 0:")
print(sorted_zero_ratings)
