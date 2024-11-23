import logging
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

# Configure basic logging
logging.basicConfig(
    filename="app.log",  # File name for the log
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    filemode="w",  # (use 'a' to append, 'w' to overwrite)
)


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

    logger = logging.getLogger("FileLogger")

    # used to iterate through recommendations and associated diagnosis
    recommendation_dict = {
        "continue": [
            "Barrett's Esophagus",
            "Chronic NSAID used with bleeding risk",
            "Severe esophagitis",
            "Documented history of bleeding GUI ulcer",
        ],
        "stop": [
            "Peptic Ulcer Disease treated 2 2-12 weeks (from NSAID; H. pylori)",
            "Upper GI symptoms without endoscopy; asmptomatic for 3 consecutive days"
            "ICU Stress Ulcer prophylaxis treated beyond ICU admission",
            "Uncomplicated H. pylori treated for 2 weeks and asymptomatic",
        ],
        "deprescribe": [
            "Mild to moderate esophagitis",
            "GERD treated for 4-8 weeks (esophagitis healed, symptoms controlled)",
        ],
    }

    llm_agent = llmAgent(groq_key=groq_key, data_path=data_path)

    # track the number of tokens used
    final_recommendation = "deprescribe"
    exit_bool = False
    token_usage = 0
    search_history_so_far = {}
    token_count_history = {}

    logger.info("Start loop 1...")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # #   Diagnosis & Encounters Information Source   # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    for recommendation_str, diagnosis_list in recommendation_dict.items():
        logger.info(f"rec: {recommendation_str}, diagnosis: {diagnosis_list}")
        # # # # # # # # # # # # # # # # # # # # # # #
        # # #   Diagnosis Information Source    # # #
        # # # # # # # # # # # # # # # # # # # # # # #
        # get diagnosis source data
        diagnosis_data_dict = llm_agent.get_data(
            encounter_key=encounter_key, source="diagnosis"
        )
        # extract information
        diagnosis_dict, diagnosis_token_count = llm_agent.extract_without_RAG(
            data_dict=diagnosis_data_dict, diagnosis_searched_for=diagnosis_list
        )

        # format boolean
        diagnosis_source_bool = llmAgent.get_bool(diagnosis_dict["diagnosis_boolean"])

        # store the bool, explanation and token count
        search_history_so_far[f"diagnosis_source_{recommendation_str}"] = diagnosis_dict
        token_count_history[f"diagnosis_source_{recommendation_str}"] = (
            diagnosis_token_count
        )

        # track overall token usage
        token_usage += diagnosis_token_count

        logger.info(f"diagnosis_source_bool: {diagnosis_source_bool}")
        logger.info(f"diagnosis_dict: {diagnosis_dict}")
        logger.info(f"diagnosis_token_count: {diagnosis_token_count}")

        # early exit opportunity
        if diagnosis_source_bool:
            exit_bool = True
            final_recommendation = recommendation_str
            logger.info("early break from loop 1!!!")
            break

        # # # # # # # # # # # # # # # # # # # # # # #
        # # #   Encounters Information Source   # # #
        # # # # # # # # # # # # # # # # # # # # # # #
        # get encounters source data
        encounters_data_dict = llm_agent.get_data(
            encounter_key=encounter_key, source="encounters"
        )
        # extract information
        encounters_dict, encounters_token_count = llm_agent.extract_without_RAG(
            data_dict=encounters_data_dict, diagnosis_searched_for=diagnosis_list
        )

        # format boolean
        encounters_source_bool = llmAgent.get_bool(encounters_dict["diagnosis_boolean"])

        # store the bool, explanation and token count
        search_history_so_far[f"encounters_source_{recommendation_str}"] = (
            encounters_dict
        )
        token_count_history[f"encounters_source_{recommendation_str}"] = (
            encounters_token_count
        )

        # track overall token usage
        token_usage += encounters_token_count

        logger.info(f"encounters_source_bool: {encounters_source_bool}")
        logger.info(f"encounters_dict: {encounters_dict}")
        logger.info(f"encounters_token_count: {encounters_token_count}")

        # early exit opportunity
        if encounters_source_bool:
            exit_bool = True
            final_recommendation = recommendation_str
            logger.info("early break from loop 1!!!")
            break

    # # # # # # # # # # # # # # # # # # # # #
    # # #   Notes Information Source    # # #
    # # # # # # # # # # # # # # # # # # # # #
    # make sure not to enter the notes loop unless a diagnosis has yet to be found
    if not exit_bool:
        logger.info("loop 2")
        for recommendation_str, diagnosis_list in recommendation_dict.items():
            logger.info(f"rec: {recommendation_str}, diagnosis: {diagnosis_list}")
            # get notes source data
            noteText = llm_agent.get_data(encounter_key=encounter_key, source="notes")
            # extract information
            notes_dict, notes_token_count = llm_agent.extract_RAG(
                noteText=noteText, diagnosis_searched_for=diagnosis_list
            )

            # format boolean
            notes_source_bool = llmAgent.get_bool(notes_dict["diagnosis_boolean"])

            # store the bool, explanation and token count
            search_history_so_far[f"notes_source_{recommendation_str}"] = notes_dict
            token_count_history[f"notes_source_{recommendation_str}"] = (
                notes_token_count
            )

            # track overall token usage
            token_usage += notes_token_count

            logger.info(f"notes_source_bool: {notes_source_bool}")
            logger.info(f"notes_dict: {notes_dict}")
            logger.info(f"notes_token_count: {notes_token_count}")

            # early exit opportunity
            if notes_source_bool:
                final_recommendation = recommendation_str
                logger.info("\n\nearly break from loop 2!!!\n\n")
                break

    # summary of explanation
    final_reasoning, summary_token_count = llm_agent.summarize_reasonings(
        recommendation_str=final_recommendation,
        search_history_so_far=search_history_so_far,
    )
    token_usage += summary_token_count
    token_count_history["final_summary"] = summary_token_count

    logger.info(f"final_recommendation: {final_recommendation}")
    logger.info(f"final_reasoning: {final_reasoning}")
    logger.info(f"token_usage: {token_usage}")
    logger.info(f"search_history_so_far: {search_history_so_far}")
    logger.info(f"token_count_history: {token_count_history}")

    return (
        final_recommendation,
        final_reasoning,
        token_usage,
        search_history_so_far,
        token_count_history,
    )


if __name__ == "__main__":
    main()
    main()
