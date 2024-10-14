from pathlib import Path

from extraction import llmAgent
from ppi_deprescribe import merge_results, ppi_deprescribe


def main(
    groq_key="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",
    data_path=Path(
        "/Users/yarg/Library/CloudStorage/OneDrive-Personal/Documents/GitHub/DataSci210_MedicationDeprescriber/Data"
    ),
):
    encounter_key = "D6253A5CE371EA"

    # extract information
    llm_agent = llmAgent(groq_key=groq_key, data_path=data_path)

    results_dict = {
        "diagnosis_dict": llm_agent.extract_diagnosis(encounter_key=encounter_key),
        "encounter_dict": llm_agent.extract_encounter_info(encounter_key=encounter_key),
        # Is the reasoning in the json or sepearte?
        # Should the reasoning be included in any of them or just the diangosis with the reasoning seperate?
        "notes_dict": llm_agent.extract_notes(encounter_key=encounter_key),
    }

    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    final_dict = merge_results(results_dict=results_dict)

    # feed the three reasonings to LLM to get a single summary
    final_reasoning = llm_agent.summarize_reasonings(results_dict=results_dict)

    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = ppi_deprescribe(patient_diagnosis=final_dict)

    print("Recommendation: ")
    print(recommendation_str)
    print("\nReasoning: ")
    print(final_reasoning)

    # # #   Metrics   # # #
    # get a single row DataFrame of the key, explanation and recommendation
    # consider:
    #   the final recommendation_str (eval as a 3 class classification)
    #   the final reasoning (evaluate how reasonable the reasoning is)
    label_df = llm_agent.data_loader.get_label_df(encounter_key=encounter_key)
    print("\nLabel df: ")
    print(label_df)


if __name__ == "__main__":
    main()
