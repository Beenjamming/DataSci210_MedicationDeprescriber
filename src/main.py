import logging
from pathlib import Path
from deprescribing_agent import DeprescribingAgent

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
