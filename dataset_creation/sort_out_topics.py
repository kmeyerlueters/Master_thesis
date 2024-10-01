# No. 2
import pandas as pd

# Pfad zur Eingabedatei
input_file_path = '../filtered_arguments_id.csv'  
# Pfad zur Ausgabedatei
output_file_path = '../filtered_arguments_topic.csv'  

# Liste der Topics, die ausgeschlossen werden sollen
topics_to_exclude = [
    'Surrogacy should be banned',
    'The vow of celibacy should be abandoned',
    'We should abandon marriage',
    'We should adopt gender-neutral language',
    'We should end affirmative action',
    'We should legalize polygamy',
    'We should legalize prostitution',
    'We should legalize sex selection',
    'We should prohibit women in combat',
    'We should subsidize stay-at-home dads',
    'We should end racial profiling',
    'We should close Guantanamo Bay detention camp',
    'We should cancel pride parades'
]

# Trennzeichen und Kodierung
data = pd.read_csv(input_file_path, delimiter=';', encoding='utf-8')

# Filtern der Daten, um nur die Zeilen zu behalten, deren Thema nicht in der Ausschlussliste steht
filtered_data = data[~data['topic'].isin(topics_to_exclude)].copy()

# Zeilenumbrüche in allen Textspalten
filtered_data['argument'] = filtered_data['argument'].apply(lambda x: x.replace('\n', ' ').replace('\r', ' ') if isinstance(x, str) else x)

# Speichern des gefilterte Datasets in einer neuen CSV-Datei, wieder mit einem Semikolon als Trennzeichen
filtered_data.to_csv(output_file_path, sep=';', index=False, encoding='utf-8')
