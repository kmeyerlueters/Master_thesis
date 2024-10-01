import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the CSV file
file_path = 'input_file'
data = pd.read_csv(file_path, delimiter=';')

# Define the gender versions you want to compare
versions = [
'Neutral', 
'Male', 'Female', 
'Trans woman', 'Trans man', 'Trans person', 
'Cis person', 'Cis woman', 'Cis man',
'Black person', 'White person', 'Person of color',
'Black Male', 'Black Female', 'White Male', 'White Female', 
'Black Trans Woman', 'Black Trans Man', 'Black Cis Woman', 'Black Cis Man', 
'White Trans Woman', 'White Trans Man', 'White Cis Woman', 'White Cis Man'
]

# Filter the data to include only the gender versions
data_gender = data[(data['Version'].isin(versions)) & (data['average_extracted_number'] != 0)]

# Perform ANOVA (necessary before Tukey's HSD)
model = ols('average_extracted_number ~ Version', data=data_gender).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA Results:")
print(anova_table)

# Perform Tukey's HSD test
tukey = pairwise_tukeyhsd(endog=data_gender['average_extracted_number'],     # Data
                          groups=data_gender['Version'],                     # Groups
                          alpha=0.05)                                        # Significance level

# Print the results
print("\nTukey's HSD Results:")
print(tukey)

# Plot the results
tukey.plot_simultaneous(figsize=(10, 6))
