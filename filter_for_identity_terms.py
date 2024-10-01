# No. 1
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define unwanted phrases
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

def identify_and_save_arguments_with_identity_terms(row, csv_writer):
    # Extracting the argument and topic from the row
    argument = row[0]
    
    # Check if any unwanted phrase is in the argument
    if any(phrase in argument.lower() for phrase in unwanted_phrases):
        return  # Skip this argument
    
    # Tokenize the text into words
    words = word_tokenize(argument)
    
    # Perform part-of-speech tagging
    tagged_words = pos_tag(words)
    
# Identify personal pronouns and gender-specific terms
    identity_terms = [word.lower() for word, pos in tagged_words if word.lower() in [
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
    'queer',
    'black', 'white', 'asian'
    'african american', 'anglo american',
    'african-american', 'anglo-american',
    'afro-american',
    'african', 'american'
    'afroamericans', 'angloamericans',
    'negroes', 'caucasians',
    'dark-skin', 'light-skin',
    'dark skin', 'light skin',
    'person', 'people'
]]
    
    # Identify personal pronouns and gender-specific terms
    found_identity_terms = [word.lower() for word, pos in tagged_words if word.lower() in identity_terms]
    
    if found_identity_terms:
        # Write the argument and topic separated by a semicolon
        csv_writer.writerow(row)

# Example: Reading from a CSV file and writing to another
input_csv_path = '/arg_quality_rank_30k.csv'
output_csv_path = 'output.csv'

with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # Input file delimiter
        csv_writer = csv.writer(output_csv_file, delimiter=';')  # Output file delimiter
        
        # Write headers for the output CSV if needed
        headers = next(csv_reader) 
        csv_writer.writerow(headers)
        
        # Skip the header row of the input file if it has one
        next(csv_reader, None)
        
        for row in csv_reader:
            # Identify and save arguments with identity terms along with the topic
            identify_and_save_arguments_with_identity_terms(row, csv_writer)
