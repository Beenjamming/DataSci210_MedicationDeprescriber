import logging
from pathlib import Path

from deprescribing_agent import DeprescribingAgent

# Configure basic logging
logging.basicConfig(
    filename="app.log",  # File name for the log
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    filemode="a",  # (use 'a' to append, 'w' to overwrite)
)


def main(
    groq_key="",
    data_path=Path(""),
    encounter_key="",
    llm_name="llama-3.3-70b-versatile",
    context_column="NoteText",
):
    """Main method containing the recommendation dictionary configured for the Proton Pump Inhibitor (PPI) medication class. The recommendation
    dictionary defines the recommendations considered and their associated diagnosis conditions.

    System activity is logged to src/app.log.

    Parameters
    ----------
    groq_key : str
        groq api key
    data_path : python Path object
        path object to data folder
    encounter_key : str
        the encounter key for the patient data to query
    llm_name : str
        the name of the llm available through groq
    context_column : str
        in terms of the clinician notes, whether to consider the LLM summary in addition to the full clinician note text
        or just consider the LLM summary

    Outputs
    ----------
    final_recommendation : str
        the final recommendation as (defined as one of the keys in the recommendation_dict)
    final_explanation : str
        the final summary of the recommendation and explanation
    token_usage : int
        the number of tokens used across the system activity
    search_history_thus_far_list : list
        a list of dictionaries, one dictionary per pair or recommendation and patient data source considered. Search results and metadata are logged and summarized into
        the final explanation. A more detailed log of activity can be viewed in the system log at src/app.log.
    token_count_history : dict
        a dictionary containing keys indicating the search step and counts of the token count used at each step as the values
    """

    logger = logging.getLogger("FileLogger")

    # used to iterate through recommendations and associated diagnosis
    recommendation_dict = {
        "continue": [
            "Barretts Esophagus or esophageal cell changes",
            "Chronic Non-Steroidal Anti Inflammatory (NSAID) use or GI prophylaxis NSAID use",
            "Severe esophagitis including bleeding esophagitis or esophageal ulcer",
            "History of gastrointestinal bleeding, gastric ulcer, upper GI bleed, or peptic ulcer hemorrhage",
        ],
        "stop": [
            "Peptic Ulcer Disease or Gastroduodenal ulcer treated for 2 - 12 weeks caused from H Pylori infection or NSAID use without bleeding",
            "Upper GI Symptoms such as reflux, difficulty swallowing, nausea, or vomiting without endoscopy - asymptomatic for 3 consecutive days",
            "ICU Stress Ulcer Prophylaxis",
            "Completed Heliobacter Pylori (H. Pylori) infection treated for 14 days with combination therapy",
        ],
        "deprescribe": [
            "Mild to moderate esophagitis or esophageal inflammation",
            "Treated Gastroesophageal Reflux Disease (GERD) or reflux symptoms such as acid reflux, heartburn, or regurgitation",
        ],
    }

    deprescribing_agent = DeprescribingAgent(
        groq_key=groq_key,
        data_path=data_path,
        logger=logger,
        llm_name=llm_name,
        context_column=context_column,
    )

    (
        final_recommendation,
        final_explanation,
        token_usage,
        search_history_thus_far_list,
        token_count_history,
    ) = deprescribing_agent.make_recommendation(
        encounter_key=encounter_key, recommendation_dict=recommendation_dict
    )

    return (
        final_recommendation,
        final_explanation,
        token_usage,
        search_history_thus_far_list,
        token_count_history,
    )


if __name__ == "__main__":
    main()
