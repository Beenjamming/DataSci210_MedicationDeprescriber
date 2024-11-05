# Define the possible keys

from fuzzywuzzy import process


ppi_keys = [
    "Barretts Esophagus",
    "Chronic NSAID use with bleeding risk",
    "Severe esophagitis",
    "Documented history of bleeding GI ulcer",
    "Mild to moderate esophagitis",
    "GERD",
    "Peptic Ulcer Disease",
    "ICU Stress Ulcer Prophylaxis",
    "H pylori infection",
    "Reasoning"
]


def update_keys_with_fuzzy_matching(input_dict: dict, threshold: int = 80) -> dict:
    """
    Update the keys of the input dictionary using fuzzy matching against a list of possible keys.

    Args:
        input_dict (dict): The dictionary with keys to be updated.
        possible_keys (list): A list of possible correct keys.
        threshold (int): The similarity score threshold for matching.

    Returns:
        dict: A new dictionary with updated keys.
    """
    updated_dict = {}
    for key, value in input_dict.items():
        match, score = process.extractOne(key, ppi_keys)
        if score >= threshold:
            updated_dict[match] = value
        else:
            print('this key not in fuzzy:',key)
            updated_dict[key] = value  # Keep the original key if no good match is found
    return updated_dict



def ppi_deprescribe(patient_diagnosis: dict):
    """Given a patient diagnosis dictionary, recommend that the PPI be continued, decreased at a lower dose, or stopped.

    Inputs:
        patient_diagnosis: dict
            dictionary of patient diagnosis booleans
    Returns:
        recommendation: str
            recommendation in the form of a string: "continue", "decrease", "stop"

    source: https://deprescribing.org/wp-content/uploads/2018/08/ppi-deprescribing-algorithm_2018_En.pdf
    """
    recommendation_dict = ["continue", "deprescribe", "stop"]
    recommendation = -1


    # check for continue PPI criteria
    if patient_diagnosis["Barretts Esophagus"]:
        recommendation = 0
    if patient_diagnosis["Chronic NSAID use with bleeding risk"]:
        recommendation = 0
    if patient_diagnosis["Severe esophagitis"]:
        recommendation = 0
    if patient_diagnosis["Documented history of bleeding GI ulcer"]:
        recommendation = 0
    if recommendation == 0:
        return recommendation_dict[recommendation]

    # Check for decrease but continue PPI criteria
    if patient_diagnosis["Mild to moderate esophagitis"]:
        recommendation = 1
    if patient_diagnosis["GERD"]:
        recommendation = 1
    if recommendation == 1:
        return recommendation_dict[recommendation]

    # check for stop PPI criteria
    if patient_diagnosis["Peptic Ulcer Disease"]:
        recommendation = 2
    if patient_diagnosis["Chronic NSAID use with bleeding risk"]:
        recommendation = 2
    if patient_diagnosis["ICU Stress Ulcer Prophylaxis"]:
        recommendation = 2
    if patient_diagnosis["H pylori infection"]:
        recommendation = 2    
    if recommendation == 2:
        return recommendation_dict[recommendation]

    # if PPI cause is still unknown, recommend decrease
    if recommendation == -1:
        recommendation = 1

    return recommendation_dict[recommendation]


def merge_results(results_dict: dict):
    """ """
    diagnosis_dict = update_keys_with_fuzzy_matching(results_dict["diagnosis_dict"])
    encounter_dict = update_keys_with_fuzzy_matching(results_dict["encounter_dict"])
    notes_dict = update_keys_with_fuzzy_matching(results_dict["notes_dict"])
    final_dict = {}
        # Collect all unique keys from the three dictionaries
    all_keys = set(diagnosis_dict.keys()).union(encounter_dict.keys(), notes_dict.keys())

    for key in all_keys:
        if key != "Reasoning":
            # Use the get method to handle missing keys, defaulting to False
            diagnosis_bool = diagnosis_dict.get(key, False)
            encounter_bool = encounter_dict.get(key, False)
            notes_bool = notes_dict.get(key, False)

            # Set the final value to True if any of the values are True
            final_dict[key] = diagnosis_bool or encounter_bool or notes_bool

    return final_dict


