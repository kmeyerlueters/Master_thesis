import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the CSV file
file_path = 'input_file'
data = pd.read_csv(file_path, delimiter=';')

# Define the group mappings
group_mappings = {
    'Neutral': 'Neutral',
    'Male': 'Gender', 
    'Female': 'Gender', 
    'Trans woman': 'Gender', 
    'Trans man': 'Gender', 
    'Trans person': 'Gender', 
    'Cis person': 'Gender', 
    'Cis woman': 'Gender', 
    'Cis man': 'Gender',
    'Black person': 'Race', 
    'White person': 'Race', 
    'Person of color': 'Race',
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
    'White Cis Man': 'Intersectional',
}

# Map the versions to their respective groups
data_gender_grouped = data[data['Version'].isin(group_mappings.keys()) & (data['average_extracted_number'] != 0)]
data_gender_grouped['Group'] = data_gender_grouped['Version'].map(group_mappings)

# Perform ANOVA (necessary before Tukey's HSD)
model = ols('average_extracted_number ~ Group', data=data_gender_grouped).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA Results:")
print(anova_table)

# Perform Tukey's HSD test
tukey = pairwise_tukeyhsd(endog=data_gender_grouped['average_extracted_number'],  # Data
                          groups=data_gender_grouped['Group'],                    # Groups
                          alpha=0.05)                                             # Significance level

# Print the results
print("\nTukey's HSD Results:")
print(tukey)

# Plot the results
tukey.plot_simultaneous(figsize=(10, 6))
