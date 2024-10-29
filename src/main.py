from pathlib import Path

from extraction import llmAgent
from ppi_deprescribe import merge_results, ppi_deprescribe


def main(
    groq_key="",
    data_path=Path(""),
    encounter_key="",
):
    """Main method

    Parameters
    ----------
    groq_key : str, optional
        groq api key, by default ""
    data_path : _type_, optional
        path object to data folder, by default Path( "" )
    encounter_key : str, optional
        the encounter key for the patient data, by default ""
    """

    # extract information
    llm_agent = llmAgent(groq_key=groq_key, data_path=data_path)

    diagnosis_json, diagnosis_token_count = llm_agent.extract_diagnosis(
        encounter_key=encounter_key
    )
    encounter_json, encounter_token_count = llm_agent.extract_encounter_info(
        encounter_key=encounter_key
    )
    # NOTE notes_context is a list of Document objects for RAGAs metrics
    notes_json, notes_token_count, notes_context = llm_agent.extract_notes(
        encounter_key=encounter_key
    )

    results_dict = {
        "diagnosis_dict": diagnosis_json,
        "encounter_dict": encounter_json,
        "notes_dict": notes_json,
    }

    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    final_dict = merge_results(results_dict=results_dict)

    # feed the three reasonings to LLM to get a single summary
    final_reasoning, reasoning_summary_token_count = llm_agent.summarize_reasonings(
        results_dict=results_dict
    )

    # count tokens used by LLM queries
    total_token_count = (
        diagnosis_token_count
        + encounter_token_count
        + notes_token_count
        + reasoning_summary_token_count
    )

    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = ppi_deprescribe(patient_diagnosis=final_dict)

    print("Recommendation: ")
    print(recommendation_str)
    print("\nReasoning: ")
    print(final_reasoning)
    print("\nTotal Token Count: ")
    print(total_token_count)

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
