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
    if patient_diagnosis["Barrett's Esophagus"]:
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
    if patient_diagnosis["Uncomplicated H. pylori"]:
        recommendation = 2
    if recommendation == 2:
        return recommendation_dict[recommendation]

    # if PPI cause is still unknown, recommend decrease
    if recommendation == -1:
        recommendation = 1

    return recommendation_dict[recommendation]


def merge_results(results_dict: dict):
    """ """
    diagnosis_dict = results_dict["diagnosis_dict"]
    encounter_dict = results_dict["encounter_dict"]
    notes_dict = results_dict["notes_dict"]

    final_dict = {}
    for key in diagnosis_dict.keys():
        if not key == "Reasoning":
            diagnosis_bool = diagnosis_dict[key]
            encounter_bool = encounter_dict[key]
            notes_bool = notes_dict[key]

            final_dict[key] = diagnosis_bool or encounter_bool or notes_bool

    return final_dict
