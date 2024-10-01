import pandas as pd
import numpy as np
from scipy import stats

# Load the dataset
file_path = '/input'  # Replace with your file path
df = pd.read_csv(file_path, delimiter=';')

# Berechne die Standardabweichung der drei Prompt-Outputs für jedes Argument
df['std_dev_prompts'] = df[['extracted_number_1', 'extracted_number_2', 'extracted_number_3']].std(axis=1)

# Berechne den Durchschnitt der Standardabweichungen über alle Argumente
average_std_dev = df['std_dev_prompts'].mean()

# Funktion zum Berechnen des Konfidenzintervalls
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)  # Standardfehler des Mittelwerts
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)  # Berechne den Fehler für das Konfidenzintervall
    return mean, mean - h, mean + h

# Berechne das Konfidenzintervall für den Mittelwert der Standardabweichungen
mean_std_dev, ci_low, ci_high = confidence_interval(df['std_dev_prompts'])

# Ausgabe des Ergebnisses
print(f"Durchschnittliche Standardabweichung über alle Argumente: {average_std_dev}")
print(f"95%-Konfidenzintervall: ({ci_low}, {ci_high})")

# Optional: Speichere das Ergebnis in einer CSV-Datei
overall_results_df = pd.DataFrame({
    'average_std_dev': [mean_std_dev],
    'confidence_interval_low': [ci_low],
    'confidence_interval_high': [ci_high]
})
overall_results_df.to_csv('output_file', sep=';', index=False)

print("Durchschnittliche Standardabweichung und Konfidenzintervalle gespeichert in 'Phi_average_std_dev_with_confidence_intervals.csv'.")


