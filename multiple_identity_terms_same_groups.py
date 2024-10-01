# count number of identity terms and how many there are in each group (multiple identity terms within the same group are counted here)

import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define unwanted phrases to filter out phrases that don't indicate identity categories
unwanted_phrases = [
    'a little white', 'african communities', 'american academy', 'american aancer society', 
    'american casualties', 'american constitutional right', 'american dream', 'american flag', 
    'american icon', 'american laws', 'american lives', 'american military', 'american prison', 
    'american public', 'american right', 'american soil', 'american symbol', 'american Values', 
    'american Way', 'back in the black', 'big brother', 'black and white', 'black mark', 'black market', 
    'black parade', 'blackboard', 'hit man', 'hit men', 'man made', 'mother cell', 
    'trans fat', 'un american', 'un-american', 'white blouse', 'whiteboard', 'white christian lands', 
    'white collar', 'white mentality', 'white noise', 'white parade', 'white supremacy', 
    'white supremacists', 'white whale'
]

# Define identity categories
gender_terms = {
    'woman', 'man',
    'women', 'men',
    'girl', 'boy',
    'mother', 'father',
    'daughter', 'son',
    'wife', 'husband',
    'niece', 'nephew',
    'mom', 'dad',
    'bride',
    'lady', 'gentleman',
    'madam', 'sir',
    'female', 'male',
    'aunt', 'uncle',
    'sister', 'brother',
    'hostess',
    'she', 'he',
    'cisgender',
    'latinx',
    'two-spirit',
    'transgender',
    'trans',
    'enby',
    'nonbinary',
    'gender non-conforming',
    'genderqueer',
    'queer'
}
race_terms = {
    'black', 'white', 'asian'
    'african american', 'anglo american',
    'african-american', 'anglo-american',
    'afro-american',
    'african', 'american'
    'afroamericans', 'angloamericans',
    'negroes', 'caucasians',
    'dark-skin', 'light-skin',
    'dark skin', 'light skin',
}
neutral_terms = {'person', 'people'}

def identify_and_save_arguments_with_identity_terms(row, csv_writer):
    argument = row[0]
    
    # Check if any unwanted phrase is in the argument
    if any(phrase in argument.lower() for phrase in unwanted_phrases):
        return  # Skip this argument
    
    # Tokenize and tag the text
    words = word_tokenize(argument)
    tagged_words = pos_tag(words)

    # Extract identity terms found in the text
    found_terms = set(word.lower() for word, _ in tagged_words if word.lower() in gender_terms | race_terms | neutral_terms)

    # Determine category based on the found terms
    categories = []
    if any(word in found_terms for word in gender_terms):
        categories.append('Gender')
    if any(word in found_terms for word in race_terms):
        categories.append('Race')
    if any(word in found_terms for word in neutral_terms):
        categories.append('Neutral')
    
    # Combine categories or list individual terms when multiple are found
    if len(found_terms) > 1:
        category = 'Multiple Terms: ' + ', '.join(found_terms)
    elif categories:
        category = ' or '.join(categories)  # Join categories for single term
    else:
        category = 'Uncategorized'

    # Write the argument, category, and original row data to the output CSV
    csv_writer.writerow(row + [category])

# File paths setup
input_csv_path = '../filtered_arguments_topic.csv'
output_csv_path = '../multiple_identites_filtered.csv'

# Processing the CSV files
with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        csv_writer = csv.writer(output_csv_file, delimiter=';')  # Change to semicolon delimiter
        
        headers = next(csv_reader)  # Assuming the first row is the header
        csv_writer.writerow(headers + ['Category'])  # Extend headers with 'Category'
        
        for row in csv_reader:
            identify_and_save_arguments_with_identity_terms(row, csv_writer)
