from extraction_agents import LLMAgent
from ppi_deprescribe import PPIDeprescribe

def main():
    
    # extract information
    llm_agent = LLMAgent(groq_key=, data_path=)
    
    diagnosis_json = llm_agent.extract_diagnosis(encounter_key=)
    
    encounter_json = llm_agent.extract_encounter_info(encounter_key=)
    
    # Is the reasoning in the json or sepearte?
    # Should the reasoning be included in any of them or just the diangosis with the reasoning seperate?
    notes_json = llm_agent.extract_notes(encounter_key=)
    
    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    
    
    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = PPIDeprescribe(patient_diagnosis=)
    
    # # #   Metrics   # # #
