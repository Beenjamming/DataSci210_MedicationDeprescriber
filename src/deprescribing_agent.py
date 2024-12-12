from extraction import ExtractionAgent
from search_patient_history import SearchPatientHistory


class DeprescribingAgent:
    """
    This script contains abstractions around the deprescribing agent process.
    See extraction.py for the extraction specific steps.
    """

    def __init__(self, groq_key, data_path, logger, llm_name=None, context_column=None):
        self.logger = logger

        # LLM model
        if llm_name is None:
            self.llm_name = "llama-3.3-70b-versatile"  # "llama-3.1-70b-versatile"
        else:
            self.llm_name = llm_name

        if context_column is None:
            self.context_column = "llm_summary"
        else:
            self.context_column = context_column

        self.llm_agent = ExtractionAgent(
            groq_key=groq_key,
            data_path=data_path,
            logger=logger,
            llm_name=self.llm_name,
        )

    def make_recommendation(self, encounter_key, recommendation_dict):
        """
        Given a patient encounter key and recommendaiton dictionary, make a recommendation and provide a final explanation.

        Parameters
        ----------
        encounter_key : str
            the encounter key for the patient data to query
        recommendation_dict : dict
            python dictionary where the keys define the recommendations considered and their values are lists of strings defining
            associated patient diagnosis information to search for

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
        search_patient = SearchPatientHistory(
            encounter_key=encounter_key,
            recommendation_dict=recommendation_dict,
            logger=self.logger,
            llm_agent=self.llm_agent,
            context_column=self.context_column,
        )
        # search patient data
        search_patient.search_notes_source()
        search_patient.search_diagnosis_source()
        search_patient.search_encounter_source()

        # make final recommendation
        recommendation_str, final_source = search_patient.get_final_recommendation()
        self.logger.info(f"Final recommendation: {recommendation_str}")
        self.logger.info(f"Final recommendation source: {final_source}")

        self.logger.info(
            f"Diagnosis search history:\n{search_patient.search_history_thus_far_list}"
        )
        self.logger.info(
            f"Recommendation search results history:\n{search_patient.recommendation_history}"
        )

        # make final explanation summary
        final_explanation = search_patient.make_summary(
            recommendation_str=recommendation_str,
            recommendation_source=final_source,
        )
        self.logger.info(f"Final recommendation explanation: {final_explanation}")

        self.logger.info(f"Final token usage: {search_patient.token_usage}")
        self.logger.info(f"Token usage history: {search_patient.token_count_history}")

        return (
            recommendation_str,
            final_explanation,
            search_patient.token_usage,
            search_patient.search_history_thus_far_list,
            search_patient.token_count_history,
        )
