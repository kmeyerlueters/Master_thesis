import csv

# File paths setup
input_csv_path = '../multiple_identites_filtered.csv'
output_csv_path_without_multiple_identities = '../multiple_identites_removed.csv'

# Processing the CSV files
with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
    with open(output_csv_path_without_multiple_identities, 'w', newline='', encoding='utf-8') as without_multiple_identities_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        without_multiple_identities_writer = csv.writer(without_multiple_identities_file, delimiter=';')
        
        headers = next(csv_reader)  # Assuming the first row is the header
        without_multiple_identities_writer.writerow(headers)  # Write headers to new file
        
        for row in csv_reader:
            category = row[-1]  # The last column is the category
            if 'Multiple Terms' not in category and 'Race' not in category:
                without_multiple_identities_writer.writerow(row)
