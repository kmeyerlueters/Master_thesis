import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'input_file'
data = pd.read_csv(file_path, delimiter=';')

# Define the gender versions you want to include
gender_versions = [
    'Neutral', 'Black Male', 'Black Female', 'White Male', 'White Female',
    'Black Trans Woman', 'Black Trans Man', 'Black Cis Woman', 'Black Cis Man',
    'White Trans Woman', 'White Trans Man', 'White Cis Woman', 'White Cis Man',
    'Black person', 'White person', 'Person of color',
    'Black Male', 'Black Female', 'White Male', 'White Female',
    'Black Trans Woman', 'Black Trans Man', 'Black Cis Woman', 'Black Cis Man',
    'White Trans Woman', 'White Trans Man', 'White Cis Woman', 'White Cis Man'
]

# Filter the data to include only the gender versions
data_gender = data[data['Version'].isin(gender_versions)]

# Further filter to exclude rows with average_extracted_number equal to 0
data_gender = data_gender[data_gender['average_extracted_number'] != 0]

# Descriptive statistics for the gender versions
descriptive_stats = data_gender['average_extracted_number'].describe()
print("Descriptive Statistics for Gender Versions:")
print(descriptive_stats)

# Group by analysis - by Gender Version
grouped_by_version = data_gender.groupby('Version')['average_extracted_number'].mean()

print("\nGrouped by Gender Version:")
print(grouped_by_version)

# Visualization - Distribution of ratings for Gender Versions
plt.figure(figsize=(10, 6))
data_gender['average_extracted_number'].hist(bins=20)
plt.title('Distribution of Ratings for Gender Versions')
plt.xlabel('Ratings')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()

# Visualization - Average Rating by Gender Version
plt.figure(figsize=(8, 6))
grouped_by_version.plot(kind='bar', color=['blue', 'orange'])
plt.title('Average Rating by Gender Version')
plt.xlabel('Gender Version')
plt.ylabel('Average Rating')
plt.grid(True)
plt.show()
