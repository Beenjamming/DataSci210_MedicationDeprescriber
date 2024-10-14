from pathlib import Path

from extraction_agents import LLMAgent
from ppi_deprescribe import PPIDeprescribe, merge_results


def main(
    groq_key="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",
    data_path=Path(
        "/Users/yarg/Library/CloudStorage/OneDrive-Personal/Documents/GitHub/DataSci210_MedicationDeprescriber/Data"
    ),
):
    encounter_key = "D6253A5CE371EA"

    # extract information
    llm_agent = LLMAgent(groq_key=groq_key, data_path=data_path)

    diagnosis_dict = llm_agent.extract_diagnosis(encounter_key=encounter_key)

    encounter_dict = llm_agent.extract_encounter_info(encounter_key=encounter_key)

    # Is the reasoning in the json or sepearte?
    # Should the reasoning be included in any of them or just the diangosis with the reasoning seperate?
    notes_dict = llm_agent.extract_notes(encounter_key=encounter_key)

    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    final_dict = merge_results(
        results_dict={
            "diagnosis_dict": diagnosis_dict,
            "encounter_dict": encounter_dict,
            "notes_dict": notes_dict,
        }
    )

    # feed the three reasonings to LLM to get a single summary

    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = PPIDeprescribe(patient_diagnosis=final_dict)
    print(recommendation_str)

    # # #   Metrics   # # #
