# No. 3.1
import pandas as pd
import re

special_verbs = {
    'have': 'has', 'do': 'does', 'go': 'goes', 'can': 'can', 'must': 'must',
    'might': 'might', 'should': 'should', 'would': 'would', 'could': 'could',
    'made': 'made', 'will': 'will', 'are': 'is', 'may': 'may',
    # und andere spezifische Anpassungen
    # Fügen Sie hier zusätzliche unregelmäßige Verben hinzu
    'catch': 'catches', 'watch': 'watches', 'fix': 'fixes',
    'buzz': 'buzzes', 'fly': 'flies', 'try': 'tries',
    'carry': 'carries', 'kiss': 'kisses', 'wash': 'washes',
    'match': 'matches', 'teach': 'teaches', 'lose': 'loses',
    'cry': 'cries', 'dry': 'dries', 'spy': 'spies',
    'apply': 'applies', 'reply': 'replies', 'deny': 'denies',
    'buy': 'buys', 'pay': 'pays', 'say': 'says',
    'lie': 'lies', 'tie': 'ties', 'die': 'dies',
    'box': 'boxes', 'mix': 'mixes', 'fizz': 'fizzes',
    'pass': 'passes', 'dress': 'dresses', 'buzz': 'buzzes',
    'push': 'pushes', 'rush': 'rushes', 'fix': 'fixes',
    # Weiter Verben hinzufügen nach Bedarf
}

# Function to correct third-person singular verbs for 'he' or 'she'
def correct_third_person_singular_verbs(text):
    pattern = r'\b(he|she) (\w+?)(?!\w*ed\b)\b'
    def replace(match):
        pronoun = match.group(1)
        verb = match.group(2)
        if verb.lower() in ['have', 'do', 'go', 'can', 'must', 'might', 'should', 'would', 'could', 'made', 'will', 'are']:
            corrected_verb = {'have': 'has', 'do': 'does', 'go': 'goes', 'can': 'can', 'must': 'must', 
                              'might': 'might', 'should': 'should', 'would': 'would', 'could': 'could', 'made': 'made',
                              'will': 'will'}.get(verb.lower(), verb)
        else:
            corrected_verb = verb + 's' if not verb.endswith('s') else verb
        return f'{pronoun} {corrected_verb}'
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)

def correct_singular_to_plural_verbs(text):
    import re
    
    # This pattern will better capture verbs including contractions ending with 's'
    pattern = r'\b(they) (\w+?)(s|n\'t)\b'
    
    # Function to replace the third-person singular verb with the plural form
    def replace(match):
        pronoun = match.group(1)
        verb = match.group(2)
        suffix = match.group(3)
        
        # Handling the exceptions explicitly, including contractions
        exceptions = {
            'has': 'have',
            'does': 'do',
            'is': 'are',
            'goes': 'go',
            # including the contraction doesn't as a full match since it's common
            'doesn\'t': 'don\'t',
            'can\'t': 'can\'t'
        }
        
        full_verb = verb + suffix  # Reconstruct the original verb before checking exceptions
        
        # Check if the full verb is an exception and return the appropriate plural form
        if full_verb.lower() in exceptions:
            return f'{pronoun} {exceptions[full_verb.lower()]}'
        elif verb.lower() in exceptions:  # Check if the base verb without suffix is an exception
            return f'{pronoun} {exceptions[verb.lower()]}'
        # For regular verbs not covered by exceptions, assume suffix is 's' and remove it
        return f'{pronoun} {verb}'

    # Apply the regex substitution to the provided text
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


def correct_plural_possessives(text, original, gender):
    # If the original term indicates plural form, adjust 'his' or 'her' back to 'their'
    if original in ['women', 'men']:
        if gender == 'male':
            text = text.replace(' his ', ' their ')
        elif gender == 'female':
            text = text.replace(' her ', ' their ')
    return text

def correct_singular_to_plural_pronouns(text, original):
    # Check if the original term indicates plural form, adjust 'she' and 'he' to 'they'
    if original in ['women', 'men']:
        text = re.sub(r'\b(she|he)\b', 'they', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(she is|he is|she’s|he’s)\b', 'they are', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(she has|he has|she’s|he’s)\b', 'they have', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(she does|he does)\b', 'they do', text, flags=re.IGNORECASE)
        # Add more patterns as needed
    return text

def adjust_themselves(argument, gender_indicator):
    """
    Adjusts 'themselves' to 'himself' or 'herself' based on gender indicator,
    but only if the context indicates a singular subject.
    """
    # Defining patterns to check for singular context
    singular_male_pattern = re.compile(r'\b(man|boy|husband|father|son)\b', re.IGNORECASE)
    singular_female_pattern = re.compile(r'\b(woman|girl|wife|mother|daughter)\b', re.IGNORECASE)

    # Check and replace based on the gender indicator
    if gender_indicator == 'male' and singular_male_pattern.search(argument):
        return argument.replace("themselves", "himself")
    elif gender_indicator == 'female' and singular_female_pattern.search(argument):
        return argument.replace("themselves", "herself")
    
    return argument

def correct_pronouns_and_verbs(text, gender):
    import re
    
    # Definiere Muster, um zu prüfen, ob der Kontext "a man" oder "a woman" enthält
    singular_male_pattern = re.compile(r'\bson\b|\bman\b', re.IGNORECASE)
    singular_female_pattern = re.compile(r'\bdaughter\b|\bwoman\b', re.IGNORECASE)

    # Überprüfe, ob der Text die spezifischen Bedingungen erfüllt
    is_singular_male = singular_male_pattern.search(text)
    is_singular_female = singular_female_pattern.search(text)
    
    # Ersetze 'they' mit 'she' oder 'he', abhängig vom Geschlecht, aber nur wenn es sich um die erste Person Singular handelt
    if gender == 'female' and is_singular_female:
        text = re.sub(r'\bthey\b', 'she', text, flags=re.IGNORECASE)
        text = re.sub(r'\bthem\b', 'her', text, flags=re.IGNORECASE)
        text = re.sub(r'\btheir\b', 'her', text, flags=re.IGNORECASE)
        text = re.sub(r'\btheirs\b', 'hers', text, flags=re.IGNORECASE)
        text = re.sub(r'\bthemself\b', 'herself', text, flags=re.IGNORECASE)
        # text = re.sub(r'\bthey or they\b', 'she', text, flags=re.IGNORECASE)
    elif gender == 'male' and is_singular_male:
        text = re.sub(r'\bthey\b', 'he', text, flags=re.IGNORECASE)
        text = re.sub(r'\bthem\b', 'him', text, flags=re.IGNORECASE)
        text = re.sub(r'\btheir\b', 'his', text, flags=re.IGNORECASE)
        text = re.sub(r'\btheirs\b', 'his', text, flags=re.IGNORECASE)
        text = re.sub(r'\bthemself\b', 'himself', text, flags=re.IGNORECASE)

    # Ersetze das Verb nach 'she' oder 'he' um korrekte Übereinstimmung zu gewährleisten, aber wieder nur unter spezifischen Bedingungen
    if (gender == 'female' and is_singular_female) or (gender == 'male' and is_singular_male):
        def verb_correction(match):
            pronoun = match.group(1)
            verb = match.group(2)
            if verb.lower() in special_verbs:
                return f"{pronoun} {special_verbs[verb.lower()]}"
            else:
                return f"{pronoun} {verb + 's' if not verb.endswith('s') else verb}"
        text = re.sub(r'\b(she|he) (\w+?)\b', verb_correction, text, flags=re.IGNORECASE)

    return text

