import pandas as pd
import numpy as np
from scipy import stats

# Funktion zum Lesen einer CSV-Datei
def read_csv_file(file):
    try:
        return pd.read_csv(file, delimiter=';')
    except pd.errors.ParserError as e:
        print(f"Error reading {file}: {e}")
        return None

# Einlesen der CSV-Dateien
file1 = 'input_prompt_1.csv'
file2 = 'input_prompt_2.csv'
file3 = 'input_prompt_3.csv'

df1 = read_csv_file(file1)
df2 = read_csv_file(file2)
df3 = read_csv_file(file3)

# Sicherstellen, dass alle DataFrames korrekt eingelesen wurden
if df1 is None or df2 is None or df3 is None:
    raise ValueError("One or more files could not be read. Please check the file format.")

# Überprüfen, ob die erforderlichen Spalten vorhanden sind
required_columns = ['ID','argument', 'topic', 'Version', 'stance', 'extracted_number']
for col in required_columns:
    if col not in df1.columns or col not in df2.columns or col not in df3.columns:
        raise ValueError(f"One or more files do not contain the '{col}' column")

# Zusammenführen der DataFrames basierend auf 'argument', 'topic', 'Version', und 'stance'
merged_df = pd.merge(df1, df2, on=['ID','argument', 'topic', 'Version', 'stance'], suffixes=('_1', '_2'))
merged_df = pd.merge(merged_df, df3, on=['ID','argument', 'topic', 'Version', 'stance'])
merged_df.rename(columns={'extracted_number': 'extracted_number_3'}, inplace=True)

# Konvertieren der 'extracted_number'-Spalten in numerische Werte
for col in ['extracted_number_1', 'extracted_number_2', 'extracted_number_3']:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

# Berechnen des Durchschnitts
merged_df['average_extracted_number'] = (
    merged_df['extracted_number_1'] +
    merged_df['extracted_number_2'] +
    merged_df['extracted_number_3']
) / 3

# Relevante Spalten für die Ausgabe auswählen
final_df = merged_df[['ID','argument', 'topic', 'Version', 'stance', 
                      'extracted_number_1', 'extracted_number_2', 
                      'extracted_number_3', 'average_extracted_number']]

# Speichern der Ergebnisse in eine neue CSV-Datei
final_df.to_csv('output_file', index=False, sep=';')

print("Durchschnittswerte berechnet und gespeichert.")
