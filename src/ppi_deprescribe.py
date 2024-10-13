def PPIDeprescribe(patient_diagnosis: dict):
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
    if patient_diagnosis['Chronic NSAID use with bleeding risk']:
        recommendation = 0
    if patient_diagnosis['Severe esophagitis']:
        recommendation = 0 
    if patient_diagnosis['Documented history of bleeding GI ulcer']:
        recommendation = 0 
        
    # Check for decrease but continue PPI criteria
    if patient_diagnosis['Mild to moderate esophagitis']:
        recommendation = 1 
    if patient_diagnosis['GERD']:
        recommendation = 1 
        
    # check for stop PPI criteria
    if patient_diagnosis['Peptic Ulcer Disease']:
        recommendation = 2
    if patient_diagnosis['Chronic NSAID use with bleeding risk']:
        recommendation = 2 
    if patient_diagnosis['ICU Stress Ulcer Prophylaxis']:
        recommendation = 2 
        
    # if PPI cause is still unknown, recommend decrease
    if recommendation == -1:
        recommendation = 1

    return recommendation_dict[recommendation]