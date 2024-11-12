from pathlib import Path

from extraction import llmAgent

"""
Iterate through diagnosis individually, break up the ppi deprescribing algorithm to handle
one diagnosis at a time.
Order:
0: "continue"
 -  Barretts Esophagus
 -  Chronic NSAID used with bleeding risk
 -  Severe esophagitis
 -  Documented history of bleeding GUI ulcer
1: "stop"
 -  Peptic Ulcer Disease
 -  Chronic NSAID use with bleeding risk
 -  ICU Stress Ulcer Prophylaxis
 -  H Pylori infection
2: "deprescribe"
 -  Mild to moderate esophagitis
 -  GERD
if non, recommend "deprescribe"  
"""


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
    # used to iterate through recommendations and associated diagnosis
    recommendation_dict = {
        "continue": [
            "Barretts Esophagus",
            "Chronic NSAID used with bleeding risk",
            "Severe esophagitis",
            "Documented history of bleeding GUI ulcer",
        ],
        "stop": [
            "Peptic Ulcer Disease",
            "Chronic NSAID use with bleeding risk",
            "ICU Stress Ulcer Prophylaxis",
            "H Pylori infection",
        ],
        "deprescribe": [
            "Mild to moderate esophagitis",
            "GERD",
        ],
    }
    # could be used to map from recommendation strings to integers
    rec_to_int = {
        "continue": 0,
        "stop": 1,
        "deprescribe": 2,
    }

    llm_agent = llmAgent(groq_key=groq_key, data_path=data_path)

    # track the number of tokens used
    token_usage = 0
    final_bool = False
    diagnosis_dict_dict = {}
    # Loop over recommendations in their order
    # if none exits recommend "deprescribe"
    for recommendation_str, diagnosis_list in recommendation_dict.items():
        # iterate through diagnosis
        for diagnosis_str in diagnosis_list:
            diagnosis_dict = llm_agent.search(
                encounter_key=encounter_key, diagnosis=diagnosis_str
            )
            diagnosis_dict_dict[diagnosis_str] = diagnosis_dict
            # track token usage
            # TODO? track each search individually
            # token_usage += token_count

            # # #   master formatter step   # # #
            # merge the diagnosis booleans (just use OR logic for now)
            diagnosis_bool_str = diagnosis_dict["diagnosis"]["diagnosis_boolean"]
            if diagnosis_bool_str in ["True", "true"]:
                diagnosis_bool = True
            elif diagnosis_bool_str in ["False", "false"]:
                diagnosis_bool = False

            encounters_bool_str = diagnosis_dict["encounters"]["diagnosis_boolean"]
            if encounters_bool_str in ["True", "true"]:
                encounters_bool = True
            elif encounters_bool_str in ["False", "false"]:
                encounters_bool = False

            notes_bool_str = diagnosis_dict["notes"]["diagnosis_boolean"]
            if notes_bool_str in ["True", "true"]:
                notes_bool = True
            elif notes_bool_str in ["False", "false"]:
                notes_bool = False

            final_bool = diagnosis_bool or encounters_bool or notes_bool

            # break out of the loop over the diagnosis list
            if final_bool:
                break
        # break out of the loop over recommendations
        if final_bool:
            break

    # NOTE: if it never exits early then recommendation_str should still be "deprescribe"

    # summary of explanation
    final_reasoning, token_count = llm_agent.summarize_reasonings(
        recommendation_str=recommendation_str, diagnosis_dict_dict=diagnosis_dict_dict
    )

    # TODO figure out how to get the token counts easily
    # count tokens used by LLM queries
    # total_token_count = (
    #     diagnosis_token_count
    #     + encounter_token_count
    #     + notes_token_count
    #     + reasoning_summary_token_count
    # )

    # print("Recommendation: ")
    # print(recommendation_str)
    # print("\nReasoning: ")
    # print(final_reasoning)
    # print("\nTotal Token Count: ")
    # print(total_token_count)

    return recommendation_str, final_reasoning  # , total_token_count


if __name__ == "__main__":
    main()
