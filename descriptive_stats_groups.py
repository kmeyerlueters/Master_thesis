import pandas as pd

# Load your dataset into a DataFrame, specifying the delimiter as ';'
df = pd.read_csv('input_file', delimiter=';')

df = df[df['average_extracted_number'] != 0]

# Separate the 'Neutral' group
df_neutral = df[df['Version'] == 'Neutral'].copy()

# Filter out 'Neutral' version for the main grouping
df_grouped = df[df['Version'] != 'Neutral'].copy()

# Define mappings for broader categories excluding Neutral
gender_map = {
    'Male': 'Gender',
    'Female': 'Gender',
    'Trans woman': 'Gender',
    'Trans man': 'Gender',
    'Trans person': 'Gender',
    'Cis person': 'Gender',
    'Cis woman': 'Gender',
    'Cis man': 'Gender'
}

race_map = {
    'Black person': 'Race',
    'White person': 'Race',
    'Person of color': 'Race'
}

intersectional_map = {
    'Black Male': 'Intersectional',
    'Black Female': 'Intersectional',
    'White Male': 'Intersectional',
    'White Female': 'Intersectional',
    'Black Trans Woman': 'Intersectional',
    'Black Trans Man': 'Intersectional',
    'Black Cis Woman': 'Intersectional',
    'Black Cis Man': 'Intersectional',
    'White Trans Woman': 'Intersectional',
    'White Trans Man': 'Intersectional',
    'White Cis Woman': 'Intersectional',
    'White Cis Man': 'Intersectional'
}

# Apply mappings to create broader categories
df_grouped['Gender_Group'] = df_grouped['Version'].map(gender_map)
df_grouped['Race_Group'] = df_grouped['Version'].map(race_map)
df_grouped['Intersectional_Group'] = df_grouped['Version'].map(intersectional_map)

# Now calculate the aggregated descriptive statistics for each broader group

# Descriptive statistics by Gender Group
gender_group_stats = df_grouped.groupby('Gender_Group')['average_extracted_number'].agg(['mean', 'median', 'std', 'count'])
print("Descriptive Statistics by Gender Group (Aggregated):")
print(gender_group_stats)

# Descriptive statistics by Race Group
race_group_stats = df_grouped.groupby('Race_Group')['average_extracted_number'].agg(['mean', 'median', 'std', 'count'])
print("\nDescriptive Statistics by Race Group (Aggregated):")
print(race_group_stats)

# Descriptive statistics by Intersectional Group
intersectional_group_stats = df_grouped.groupby('Intersectional_Group')['average_extracted_number'].agg(['mean', 'median', 'std', 'count'])
print("\nDescriptive Statistics by Intersectional Group (Aggregated):")
print(intersectional_group_stats)

# Descriptive statistics for the 'Neutral' group
neutral_stats = df_neutral['average_extracted_number'].agg(['mean', 'median', 'std', 'count'])
print("\nDescriptive Statistics for Neutral Group:")
print(neutral_stats)