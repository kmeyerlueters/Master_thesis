# No. 3
import pandas as pd
import re

# Function to replace terms based on the provided mappings
def replace_terms(text, mapping):
    for old, new in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r'\b{}\b'.format(re.escape(old))
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)
    return text

from verb_corrections import correct_third_person_singular_verbs
from verb_corrections import correct_singular_to_plural_verbs
from verb_corrections import correct_plural_possessives
from verb_corrections import correct_singular_to_plural_pronouns
from verb_corrections import adjust_themselves
from verb_corrections import correct_pronouns_and_verbs 

# Function to create different versions of each argument
def create_transformed_arguments(data, female_to_neutral, male_to_neutral, neutral_to_female, 
                                 neutral_to_male, neutral_to_transman, neutral_to_transwoman, 
                                 neutral_to_transperson, neutral_to_cisman, neutral_to_ciswoman, 
                                 neutral_to_cisperson, neutral_to_black, neutral_to_white, 
                                 neutral_to_poc, neutral_to_black_female, neutral_to_black_male, 
                                 neutral_to_white_female, neutral_to_white_male, neutral_to_black_transwoman, 
                                 neutral_to_black_transman, neutral_to_black_ciswoman, neutral_to_black_cisman, 
                                 neutral_to_white_transwoman, neutral_to_white_transman, 
                                 neutral_to_white_ciswoman, neutral_to_white_cisman):
    transformed_data = []
    unique_id = 1  # Startwert für die eindeutige ID
    
    for _, row in data.iterrows():
        original_argument = row['argument']
        topic = row['topic']
        stance = row['stance_WA']
        
        # Neutral version
        neutral_argument = correct_singular_to_plural_verbs(replace_terms(replace_terms(original_argument, female_to_neutral), male_to_neutral))

        # Male and female versions with initial corrections
        male_argument = replace_terms(neutral_argument, neutral_to_male)
        female_argument = replace_terms(neutral_argument, neutral_to_female)

        # Transgender versions with initial corrections
        transwoman_argument = replace_terms(neutral_argument, neutral_to_transwoman)
        transman_argument = replace_terms(neutral_argument, neutral_to_transman)
        transperson_argument = replace_terms(neutral_argument, neutral_to_transperson)

        # Transgender versions with initial corrections
        # First convert both male and female terms to neutral for transwoman_argument
        cis_woman_argument = replace_terms(neutral_argument, neutral_to_ciswoman)
        cis_man_argument = replace_terms(neutral_argument, neutral_to_cisman)
        cis_person_argument = replace_terms(neutral_argument, neutral_to_cisperson)

        # Black, White and Person of color
        black_person_argument = replace_terms(neutral_argument, neutral_to_black)
        white_person_argument = replace_terms(neutral_argument, neutral_to_white)
        poc_argument = replace_terms(neutral_argument, neutral_to_poc)

        # Black Male and female versions with initial corrections
        black_male_argument = replace_terms(neutral_argument, neutral_to_black_male)
        black_female_argument = replace_terms(neutral_argument, neutral_to_black_female)

        # White Male and female versions with initial corrections
        white_male_argument = replace_terms(neutral_argument, neutral_to_white_male)
        white_female_argument = replace_terms(neutral_argument, neutral_to_white_female)

        # New: Black Trans versions
        black_transwoman_argument = replace_terms(neutral_argument, neutral_to_black_transwoman)
        black_transman_argument = replace_terms(neutral_argument, neutral_to_black_transman)
        
        # New: Black Cis versions
        black_ciswoman_argument = replace_terms(neutral_argument, neutral_to_black_ciswoman)
        black_cisman_argument = replace_terms(neutral_argument, neutral_to_black_cisman)
        
        # New: White Trans versions
        white_transwoman_argument = replace_terms(neutral_argument, neutral_to_white_transwoman)
        white_transman_argument = replace_terms(neutral_argument, neutral_to_white_transman)
        
        # New: White Cis versions
        white_ciswoman_argument = replace_terms(neutral_argument, neutral_to_white_ciswoman)
        white_cisman_argument = replace_terms(neutral_argument, neutral_to_white_cisman)

        # Correct plural possessives and pronouns based on the original context
        #Person
        transperson_argument = correct_singular_to_plural_verbs(transperson_argument)
        cis_person_argument = correct_singular_to_plural_verbs(cis_person_argument)
        black_person_argument = correct_singular_to_plural_verbs(black_person_argument)
        white_person_argument = correct_singular_to_plural_verbs(white_person_argument)
        poc_argument = correct_singular_to_plural_verbs(poc_argument)

        #Man
        male_argument = correct_plural_possessives(male_argument, 'men', 'male')
        male_argument = correct_singular_to_plural_pronouns(male_argument, 'men')
        male_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(male_argument))

        #Woman
        female_argument = correct_plural_possessives(female_argument, 'women', 'female')
        female_argument = correct_singular_to_plural_pronouns(female_argument, 'women')
        female_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(female_argument))

        #Trans Man
        transman_argument = correct_plural_possessives(transman_argument, 'men', 'male')
        transman_argument = correct_singular_to_plural_pronouns(transman_argument, 'men')
        transman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(transman_argument))

        # Trans Woman
        transwoman_argument = correct_plural_possessives(transwoman_argument, 'women', 'female')
        transwoman_argument = correct_singular_to_plural_pronouns(transwoman_argument, 'women')
        transwoman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(transwoman_argument))

        # Cis Woman
        cis_woman_argument = correct_plural_possessives(cis_woman_argument, 'women', 'female')
        cis_woman_argument = correct_singular_to_plural_pronouns(cis_woman_argument, 'women')
        cis_woman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(cis_woman_argument))

        # Cis Man
        cis_man_argument = correct_plural_possessives(cis_man_argument, 'men', 'male')
        cis_man_argument = correct_singular_to_plural_pronouns(cis_man_argument, 'men')
        cis_man_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(cis_man_argument))
        
        #Black Man
        black_male_argument = correct_plural_possessives(black_male_argument, 'men', 'male')
        black_male_argument = correct_singular_to_plural_pronouns(black_male_argument, 'men')
        black_male_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_male_argument))

        #Black Woman
        black_female_argument = correct_plural_possessives(black_female_argument, 'women', 'female')
        black_female_argument = correct_singular_to_plural_pronouns(black_female_argument, 'women')
        black_female_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_female_argument))
        
        #White Man
        white_male_argument = correct_plural_possessives(white_male_argument, 'men', 'male')
        white_male_argument = correct_singular_to_plural_pronouns(white_male_argument, 'men')
        white_male_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_male_argument))

        #White Woman
        white_female_argument = correct_plural_possessives(white_female_argument, 'women', 'female')
        white_female_argument = correct_singular_to_plural_pronouns(white_female_argument, 'women')
        white_female_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_female_argument))

        # Black Trans Woman
        black_transwoman_argument = correct_plural_possessives(black_transwoman_argument, 'women', 'female')
        black_transwoman_argument = correct_singular_to_plural_pronouns(black_transwoman_argument, 'women')
        black_transwoman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_transwoman_argument))

        # Black Trans Man
        black_transman_argument = correct_plural_possessives(black_transman_argument, 'men', 'male')
        black_transman_argument = correct_singular_to_plural_pronouns(black_transman_argument, 'men')
        black_transman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_transman_argument))

        # Black Cis Woman
        black_ciswoman_argument = correct_plural_possessives(black_ciswoman_argument, 'women', 'female')
        black_ciswoman_argument = correct_singular_to_plural_pronouns(black_ciswoman_argument, 'women')
        black_ciswoman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_ciswoman_argument))

        # Black Cis Man
        black_cisman_argument = correct_plural_possessives(black_cisman_argument, 'men', 'male')
        black_cisman_argument = correct_singular_to_plural_pronouns(black_cisman_argument, 'men')
        black_cisman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(black_cisman_argument))

        # White Trans Woman
        white_transwoman_argument = correct_plural_possessives(white_transwoman_argument, 'women', 'female')
        white_transwoman_argument = correct_singular_to_plural_pronouns(white_transwoman_argument, 'women')
        white_transwoman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_transwoman_argument))

        # White Trans Man
        white_transman_argument = correct_plural_possessives(white_transman_argument, 'men', 'male')
        white_transman_argument = correct_singular_to_plural_pronouns(white_transman_argument, 'men')
        white_transman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_transman_argument))

        # White Cis Woman
        white_ciswoman_argument = correct_plural_possessives(white_ciswoman_argument, 'women', 'female')
        white_ciswoman_argument = correct_singular_to_plural_pronouns(white_ciswoman_argument, 'women')
        white_ciswoman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_ciswoman_argument))

        # White Cis Man
        white_cisman_argument = correct_plural_possessives(white_cisman_argument, 'men', 'male')
        white_cisman_argument = correct_singular_to_plural_pronouns(white_cisman_argument, 'men')
        white_cisman_argument = correct_singular_to_plural_verbs(correct_third_person_singular_verbs(white_cisman_argument))

        # Additional adjustments for 'themselves' based on the gender
        male_argument = adjust_themselves(male_argument, 'male')
        female_argument = adjust_themselves(female_argument, 'female')
        transman_argument = adjust_themselves(transman_argument, 'male')
        transwoman_argument = adjust_themselves(transwoman_argument, 'female')
        black_male_argument = adjust_themselves(black_male_argument, 'male')
        black_female_argument = adjust_themselves(black_female_argument, 'female')
        white_male_argument = adjust_themselves(white_male_argument, 'male')
        white_female_argument = adjust_themselves(white_female_argument, 'female')
        black_transwoman_argument = adjust_themselves(black_transwoman_argument, 'female')
        black_transman_argument = adjust_themselves(black_transman_argument, 'male')
        black_ciswoman_argument = adjust_themselves(black_ciswoman_argument, 'female')
        black_cisman_argument = adjust_themselves(black_cisman_argument, 'male')
        white_transwoman_argument = adjust_themselves(white_transwoman_argument, 'female')
        white_transman_argument = adjust_themselves(white_transman_argument, 'male')
        white_ciswoman_argument = adjust_themselves(white_ciswoman_argument, 'female')
        white_cisman_argument = adjust_themselves(white_cisman_argument, 'male')
        cis_woman_argument = adjust_themselves(cis_woman_argument, 'female')
        cis_man_argument = adjust_themselves(cis_man_argument, 'male')

        # Correct pronouns and verbs based on the gender
        male_argument = correct_pronouns_and_verbs(male_argument, 'male')
        female_argument = correct_pronouns_and_verbs(female_argument, 'female')
        transman_argument = correct_pronouns_and_verbs(transman_argument, 'male')
        transwoman_argument = correct_pronouns_and_verbs(transwoman_argument, 'female')
        black_male_argument = correct_pronouns_and_verbs(black_male_argument, 'male')
        black_female_argument = correct_pronouns_and_verbs(black_female_argument, 'female')
        white_male_argument = correct_pronouns_and_verbs(white_male_argument, 'male')
        white_female_argument = correct_pronouns_and_verbs(white_female_argument, 'female')
        black_transwoman_argument = correct_pronouns_and_verbs(black_transwoman_argument, 'female')
        black_transman_argument = correct_pronouns_and_verbs(black_transman_argument, 'male')
        black_ciswoman_argument = correct_pronouns_and_verbs(black_ciswoman_argument, 'female')
        black_cisman_argument = correct_pronouns_and_verbs(black_cisman_argument, 'male')
        white_transwoman_argument = correct_pronouns_and_verbs(white_transwoman_argument, 'female')
        white_transman_argument = correct_pronouns_and_verbs(white_transman_argument, 'male')
        white_ciswoman_argument = correct_pronouns_and_verbs(white_ciswoman_argument, 'female')
        white_cisman_argument = correct_pronouns_and_verbs(white_cisman_argument, 'male')
        cis_woman_argument = correct_pronouns_and_verbs(cis_woman_argument, 'female')
        cis_man_argument = correct_pronouns_and_verbs(cis_man_argument, 'male')


        # Add the corrected arguments to the data frame
        transformed_data.extend([
            # {'argument': original_argument, 'Version': 'Original', 'topic': topic, 'ID': unique_id, },
            {'argument': neutral_argument, 'Version': 'Neutral', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': male_argument, 'Version': 'Male', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': female_argument, 'Version': 'Female', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': transwoman_argument, 'Version': 'Trans woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': transman_argument, 'Version': 'Trans man', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': transperson_argument, 'Version': 'Trans person', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': cis_person_argument, 'Version': 'Cis person', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': cis_woman_argument, 'Version': 'Cis woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': cis_man_argument, 'Version': 'Cis man', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_person_argument, 'Version': 'Black person', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_person_argument, 'Version': 'White person', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': poc_argument, 'Version': 'Person of color', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_male_argument, 'Version': 'Black Male', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_female_argument, 'Version': 'Black Female', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_male_argument, 'Version': 'White Male', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_female_argument, 'Version': 'White Female', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_transwoman_argument, 'Version': 'Black Trans Woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_transman_argument, 'Version': 'Black Trans Man', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_ciswoman_argument, 'Version': 'Black Cis Woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': black_cisman_argument, 'Version': 'Black Cis Man', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_transwoman_argument, 'Version': 'White Trans Woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_transman_argument, 'Version': 'White Trans Man', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_ciswoman_argument, 'Version': 'White Cis Woman', 'topic': topic, 'ID': unique_id, 'stance': stance},
            {'argument': white_cisman_argument, 'Version': 'White Cis Man', 'topic': topic, 'ID': unique_id, 'stance': stance}, 
        ])
        
        unique_id += 1  # Inkrementiere die ID für die nächste Gruppe

    return pd.DataFrame(transformed_data)


female_to_neutral = {
    'woman': 'person', 'women': 'people', 'mother': 'parent',
    'wife': 'spouse', 'mom': 'parent', 'female': 'individual',
    'she': 'they', 'her': 'them', 'hers': 'their', 'herself': 'themself', 'men and women': 'people', 
    'his or her': 'their', 'he or she': 'they', 'a womans': 'a persons'
}

male_to_neutral = {
    'man': 'person', 'men': 'people', 'father': 'parent',
    'husband': 'spouse', 'dad': 'parent', 'male': 'individual',
    'he': 'they', 'him': 'them', 'his': 'their', 'himself': 'themself', 'men and women': 'people', 
    'his or her': 'their', 'he or she': 'they', 'a mans': 'a persons'
}

neutral_to_female = {
    'person': 'woman', 'persons': 'women', 'people': 'women', 'teen':'girl',
    'parent': 'mother', 'spouse': 'wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a woman\'s', 'another person\'s': 'another woman\'s', 'a persons': 'a womans', 'another persons': 'another womans'
}

neutral_to_male = {
    'person': 'man', 'persons': 'men', 'people': 'men', 'teen':'boy', 
    'parent': 'father', 'spouse': 'husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a man\'s', 'another person\'s': 'another man\'s', 'a persons': 'a mans', 'another persons': 'another mans',
}

neutral_to_transwoman = {
    'person': 'trans woman', 'persons': 'trans women', 'people': 'trans women', 'teen':'trans girl', 
    'parent': 'trans mother', 'spouse': 'trans wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a trans woman\'s', 'another person\'s': 'another trans woman\'s', 'a persons': 'a trans womans', 'another persons': 'another trans womans'
}

neutral_to_transman = {
    'person': 'trans man', 'persons': 'trans men', 'people': 'trans men', 'teen':'trans boy',
    'parent': 'trans father', 'spouse': 'trans husband', 'themself': 'himself','his or her': 'his', 'a person\'s': 'a trans man\'s', 'another person\'s': 'another trans man\'s', 'a persons': 'a trans mans', 'another persons': 'another trans mans'
}

neutral_to_transperson = {
    'person': 'trans person', 'persons': 'trans persons', 'people': 'trans people', 'teen':'trans teen',
    'parent': 'trans parent', 'spouse': 'trans spouse', 'his or her': 'their', 'a trans trans person\'s': 'a trans person\'s', 'another trans trans person\'s': 'another trans person\'s', 'a trans trans persons': 'a trans persons', 'another trans trans persons': 'another trans persons'
}

neutral_to_ciswoman = {
    'person': 'cis woman', 'persons': 'cis women', 'people': 'cis women', 'teen':'cis girl', 
    'parent': 'cis mother', 'spouse': 'cis wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a cis woman\'s', 'another person\'s': 'another cis woman\'s', 'a persons': 'a cis womans', 'another persons': 'another cis womans'
}

neutral_to_cisman = {
    'person': 'cis man', 'persons': 'cis men', 'people': 'cis men', 'teen':'cis boy',
    'parent': 'cis father', 'spouse': 'cis husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a cis man\'s', 'another person\'s': 'another cis man\'s', 'a persons': 'a cis mans', 'another persons': 'another cis mans'
}

neutral_to_cisperson = {
    'person': 'cis person', 'persons': 'cis persons', 'people': 'cis people', 'teen':'cis teen',
    'parent': 'cis parent', 'spouse': 'cis spouse', 'his or her': 'their', 'a person\'s': 'a cis person\'s', 'another person\'s': 'another cis person\'s', 'a cis cis persons': 'a cis persons', 'another cis cis persons': 'another cis persons'
}

neutral_to_black = {
    'person': 'black person', 'persons': 'black persons', 'people': 'black people', 'teen':'black teen', 
    'parent': 'black parent', 'spouse': 'black spouse', 'his or her': 'their', 'a black black person\'s': 'a black person\'s', 'another black black person\'s': 'another black person\'s', 'a black black persons': 'a black persons', 'another black black persons': 'another black persons'
}

neutral_to_white = {
    'person': 'white person', 'persons': 'white persons', 'people': 'white people', 'teen': 'white teen', 
    'parent': 'white parent', 'spouse': 'white spouse', 'his or her': 'their', 'a white person\'s': 'a white person\'s', 'another white person\'s': 'another white person\'s', 'a white persons': 'a white persons', 'another white persons': 'another white persons'
}

neutral_to_poc = {
    'person': 'person of color', 'persons': 'persons of color', 'people': 'people of color', 'teen':'young person of color', 
    'parent': 'parent of color', 'spouse': 'spouse of color', 'his or her': 'their', 'a person of color of color\'s': 'a person of color\'s', 'another person of color of color\'s': 'another person of color\'s', # hier noch ein Fehler: 'a persons of color': 'a person of colors'
}

neutral_to_black_female = {
    'person': 'black woman', 'persons': 'black women', 'people': 'black women', 'teen':'black girl', 
    'parent': 'black mother', 'spouse': 'black wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a black woman\'s', 'another person\'s': 'another black woman\'s', 'a persons': 'a black womans', 'another persons': 'another black womans'
}

neutral_to_black_male = {
    'person': 'black man', 'persons': 'black men', 'people': 'black men', 'teen':'black boy', 
    'parent': 'black father', 'spouse': 'black husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a black man\'s', 'another person\'s': 'another black man\'s', 'a persons': 'a black mans', 'another persons': 'another black mans',
}

neutral_to_white_female = {
    'person': 'white woman', 'persons': 'white women', 'people': 'white women', 'teen':'white girl', 
    'parent': 'white mother', 'spouse': 'white wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a white woman\'s', 'another person\'s': 'another white woman\'s', 'a persons': 'a white womans', 'another persons': 'another white womans'
}

neutral_to_white_male = {
    'person': 'white man', 'persons': 'white men', 'people': 'white men', 'teen':'white boy', 
    'parent': 'white father', 'spouse': 'white husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a white man\'s', 'another person\'s': 'another white man\'s', 'a persons': 'a white mans', 'another persons': 'another white mans',
}

neutral_to_black_transwoman = {
    'person': 'black trans woman', 'persons': 'black trans women', 'people': 'black trans women', 'teen':'black trans girl',
    'parent': 'black trans mother', 'spouse': 'black trans wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a black trans woman\'s', 'another person\'s': 'another black trans woman\'s', 'a persons': 'a black trans womans', 'another persons': 'another black trans womans'
}

neutral_to_black_transman = {
    'person': 'black trans man', 'persons': 'black trans men', 'people': 'black trans men', 'teen':'black trans boy',
    'parent': 'black trans father', 'spouse': 'black trans husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a black trans man\'s', 'another person\'s': 'another black trans man\'s', 'a persons': 'a black trans mans', 'another persons': 'another black trans mans',
}

neutral_to_black_ciswoman = {
    'person': 'black cis woman', 'persons': 'black cis women', 'people': 'black cis women', 'teen':'black cis girl',
    'parent': 'black cis mother', 'spouse': 'black cis wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a black cis woman\'s', 'another person\'s': 'another black cis woman\'s', 'a persons': 'a black cis womans', 'another persons': 'another black cis womans'
}

neutral_to_black_cisman = {
    'person': 'black cis man', 'persons': 'black cis men', 'people': 'black cis men', 'teen':'black cis boy',
    'parent': 'black cis father', 'spouse': 'black cis husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a black cis man\'s', 'another person\'s': 'another black cis man\'s', 'a persons': 'a black cis mans', 'another persons': 'another black cis mans',
}

neutral_to_white_transwoman = {
    'person': 'white trans woman', 'persons': 'white trans women', 'people': 'white trans women', 'teen':'white trans girl',
    'parent': 'white trans mother', 'spouse': 'white trans wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a white trans woman\'s', 'another person\'s': 'another white trans woman\'s', 'a persons': 'a white trans womans', 'another persons': 'another white trans womans'
}

neutral_to_white_transman = {
    'person': 'white trans man', 'persons': 'white trans men', 'people': 'white trans men', 'teen':'white trans boy',
    'parent': 'white trans father', 'spouse': 'white trans husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a white trans man\'s', 'another person\'s': 'another white trans man\'s', 'a persons': 'a white trans mans', 'another persons': 'another white trans mans',
}

neutral_to_white_ciswoman = {
    'person': 'white cis woman', 'persons': 'white cis women', 'people': 'white cis women', 'teen':'white cis girl',
    'parent': 'white cis mother', 'spouse': 'white cis wife', 'themself': 'herself', 'his or her': 'her', 'a person\'s': 'a white cis woman\'s', 'another person\'s': 'another white cis woman\'s', 'a persons': 'a white cis womans', 'another persons': 'another white cis womans'
}

neutral_to_white_cisman = {
    'person': 'white cis man', 'persons': 'white cis men', 'people': 'white cis men', 'teen':'white cis boy',
    'parent': 'white cis father', 'spouse': 'white cis husband', 'themself': 'himself', 'his or her': 'his', 'a person\'s': 'a white cis man\'s', 'another person\'s': 'another white cis man\'s', 'a persons': 'a white cis mans', 'another persons': 'another white cis mans',
}

# Read the dataset
file_path = '../results/multiple_identites_removed.csv'
data = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

# Apply the function to the dataset
transformed_arguments = create_transformed_arguments(data, female_to_neutral, male_to_neutral, neutral_to_female, 
                                                    neutral_to_male, neutral_to_transman, neutral_to_transwoman, 
                                                    neutral_to_transperson, neutral_to_cisman, neutral_to_ciswoman, 
                                                    neutral_to_cisperson, neutral_to_black, neutral_to_white, 
                                                    neutral_to_poc, neutral_to_black_female, neutral_to_black_male, 
                                                    neutral_to_white_female, neutral_to_white_male, neutral_to_black_transwoman, 
                                                    neutral_to_black_transman, neutral_to_black_ciswoman, neutral_to_black_cisman, 
                                                    neutral_to_white_transwoman, neutral_to_white_transman, 
                                                    neutral_to_white_ciswoman, neutral_to_white_cisman)

# Save the transformed arguments to a new CSV file with semicolon delimiter
output_file_path = '../argument_versions.csv'
transformed_arguments.to_csv(output_file_path, sep=';', index=False, encoding='utf-8')

print(f"Transformed arguments have been saved to: {output_file_path}")
