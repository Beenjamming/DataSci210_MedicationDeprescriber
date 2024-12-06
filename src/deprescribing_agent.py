from extraction import ExtractionAgent


class DeprescribingAgent:
    """
    This script contains abstractions around the deprescribing agent process.
    See extraction.py for the extraction specific steps.
    """

    def __init__(self, groq_key, data_path, logger):
        self.logger = logger

        self.llm_agent = ExtractionAgent(
            groq_key=groq_key, data_path=data_path, logger=logger
        )

    def make_recommendation(self, encounter_key, recommendation_dict):
        """ """
        search_patient = SearchPatientHistory(
            encounter_key=encounter_key,
            recommendation_dict=recommendation_dict,
            logger=self.logger,
            llm_agent=self.llm_agent,
        )
        # search patient data
        search_patient.search_diagnosis_source()
        search_patient.search_encounter_source()
        search_patient.search_notes_source()

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


class SearchPatientHistory:
    """
    Abstraction of a single search of a patients history.
    """

    def __init__(self, encounter_key, recommendation_dict, logger, llm_agent):
        self.encounter_key = encounter_key
        self.recommendation_dict = recommendation_dict
        self.logger = logger
        self.llm_agent = llm_agent

        self.token_usage = 0
        self.search_history_thus_far_list = []
        self.token_count_history = {}
        self.recommendation_history = {
            "source:diagnosis": {},
            "source:encounter": {},
            "source:notes": {},
        }

    def search_diagnosis_source(self):
        """ """
        # # # # # # # # # # # # # # # # # # # # # # #
        # # #   Diagnosis Information Source    # # #
        # # # # # # # # # # # # # # # # # # # # # # #
        self.logger.info("Searching diagnosis info source...")
        for recommendation_str, diagnosis_list in self.recommendation_dict.items():
            self.logger.info(
                f" -  rec: {recommendation_str}, diagnosis: {diagnosis_list}"
            )
            # # # # # # # # # # # # # # # # # # # # # # #
            # # #   Diagnosis Information Source    # # #
            # # # # # # # # # # # # # # # # # # # # # # #
            # get diagnosis source data
            diagnosis_data_dict = self.llm_agent.get_data(
                encounter_key=self.encounter_key, source="diagnosis"
            )
            # extract information
            diagnosis_dict, diagnosis_token_count = self.llm_agent.extract_without_RAG(
                data_dict=diagnosis_data_dict, diagnosis_searched_for=diagnosis_list
            )

            # track recommendations
            self.recommendation_history["source:diagnosis"][recommendation_str] = (
                self.llm_agent.get_bool(diagnosis_dict["diagnosis_boolean"])
            )

            # add the data source to the diagnosis dict
            diagnosis_dict["source"] = "Patient diagnosis record"
            # add the recommendation and associated diagnoses
            diagnosis_dict["recommendation considered"] = recommendation_str
            diagnosis_dict["associated diagnosis list"] = self.recommendation_dict[
                recommendation_str
            ]

            # store the bool, explanation, info source, recomendation and associated diagnoses
            self.search_history_thus_far_list.append(diagnosis_dict)
            # store token count
            self.token_count_history[f"diagnosis_source_{recommendation_str}"] = (
                diagnosis_token_count
            )

            # track overall token usage
            self.token_usage += diagnosis_token_count

            self.logger.info(
                f" -  diagnosis_source_bool: {diagnosis_dict["diagnosis_boolean"]}"
            )
            self.logger.info(f" -  diagnosis_dict: {diagnosis_dict}")
            self.logger.info(f" -  diagnosis_token_count: {diagnosis_token_count}")

    def search_encounter_source(self):
        """ """
        # # # # # # # # # # # # # # # # # # # # # # #
        # # #   Encounters Information Source   # # #
        # # # # # # # # # # # # # # # # # # # # # # #
        self.logger.info("Searching encounter info source...")
        for recommendation_str, diagnosis_list in self.recommendation_dict.items():
            self.logger.info(
                f" -  rec: {recommendation_str}, diagnosis: {diagnosis_list}"
            )
            # get encounters source data
            encounters_data_dict = self.llm_agent.get_data(
                encounter_key=self.encounter_key, source="encounters"
            )
            # extract information
            encounter_dict, encounters_token_count = self.llm_agent.extract_without_RAG(
                data_dict=encounters_data_dict,
                diagnosis_searched_for=diagnosis_list,
            )

            # track recommendations
            self.recommendation_history["source:encounter"][recommendation_str] = (
                self.llm_agent.get_bool(encounter_dict["diagnosis_boolean"])
            )

            # add the data source to the diagnosis dict
            encounter_dict["source"] = "Patient encounter record"
            # add the recommendation and associated diagnoses
            encounter_dict["recommendation considered"] = recommendation_str
            encounter_dict["associated diagnosis list"] = self.recommendation_dict[
                recommendation_str
            ]

            # store the bool, explanation, info source, recomendation and associated diagnoses
            self.search_history_thus_far_list.append(encounter_dict)
            # store token count
            self.token_count_history[f"encounters_source_{recommendation_str}"] = (
                encounters_token_count
            )

            # track overall token usage
            self.token_usage += encounters_token_count

            self.logger.info(
                f" -  encounters_source_bool: {encounter_dict["diagnosis_boolean"]}"
            )
            self.logger.info(f" -  encounters_dict: {encounter_dict}")
            self.logger.info(f" -  encounters_token_count: {encounters_token_count}")

    def search_notes_source(self):
        """ """
        # # # # # # # # # # # # # # # # # # # # #
        # # #   Notes Information Source    # # #
        # # # # # # # # # # # # # # # # # # # # #
        # make sure not to enter the notes loop unless a diagnosis has yet to be found
        self.logger.info("Searching notes info source...")

        noteText = self.llm_agent.get_data(
            encounter_key=self.encounter_key, source="notes"
        )

        # Check if noteText is empty, then pre-processor found no diagnoses
        if not noteText.empty:
            # setup vectore store retriever with noteText, setup here before loop
            self.llm_agent.set_retriever(noteText)

            for recommendation_str, diagnosis_list in self.recommendation_dict.items():
                self.logger.info(
                    f" -  rec: {recommendation_str}, diagnosis: {diagnosis_list}"
                )
                # get notes source data

                # extract information
                notes_dict, notes_token_count = self.llm_agent.extract_RAG(
                    diagnosis_searched_for=diagnosis_list
                )

                # sometimes the llm returns a dict contained in a list
                # check to see if returned object is a list, if so get the first item
                if isinstance(notes_dict, list) and notes_dict:
                    self.logger.info(
                        f" -  llm returned a dict contained in a list, rec: {recommendation_str}"
                    )
                    notes_dict = notes_dict[0]

                # track recommendations
                self.recommendation_history["source:notes"][recommendation_str] = (
                    self.llm_agent.get_bool(notes_dict["diagnosis_boolean"])
                )

                # add the data source to the diagnosis dict
                notes_dict["source"] = "Patient notes history"
                # add the recommendation and associated diagnoses
                notes_dict["recommendation considered"] = recommendation_str
                notes_dict["associated diagnosis list"] = self.recommendation_dict[
                    recommendation_str
                ]

                # store the bool, explanation, info source, recomendation and associated diagnoses
                self.search_history_thus_far_list.append(notes_dict)
                # store token count
                self.token_count_history[f"notes_source_{recommendation_str}"] = (
                    notes_token_count
                )

                # track overall token usage
                self.token_usage += notes_token_count

                self.logger.info(
                    f" -  notes_source_bool: {notes_dict["diagnosis_boolean"]}"
                )
                self.logger.info(f" -  notes_dict: {notes_dict}")
                self.logger.info(f" -  notes_token_count: {notes_token_count}")
        else:
            self.logger.info(" -  No diagnoses found in notes...")

    def get_final_recommendation(self):
        """
        Get the final recommendation using the recommendation_dict.

        This prioritizes a determination from the patient diagnosis data over encounter data over notes.
        It prioritizes recommendations of continue, stop, then deprescribe.
        """
        trip_bool = False
        final_recommendation = "deprescribe"
        final_source = None
        for source_key, rec_dict in self.recommendation_history.items():
            for rec_key, rec_bool in rec_dict.items():
                if rec_bool:
                    # break inner loop and set trip_bool=True to break outer loop
                    trip_bool = True
                    final_recommendation = rec_key
                    final_source = source_key
                    break
            if trip_bool:
                # if trip_bool True then break loop
                break

        return final_recommendation, final_source

    def make_summary(self, recommendation_str, recommendation_source):
        """ """
        # summary of explanation
        final_explanation, summary_token_count = self.llm_agent.summarize_reasonings(
            recommendation_str=recommendation_str,
            recommendation_source=recommendation_source,
            search_history_so_far=self.search_history_thus_far_list,
        )
        self.token_usage += summary_token_count
        self.token_count_history["final_summary"] = summary_token_count

        self.logger.info(f"final_explanation: {final_explanation}")
        self.logger.info(f"token_usage: {self.token_usage}")
        self.logger.info(f"search_history_so_far: {self.search_history_thus_far_list}")
        self.logger.info(f"token_count_history: {self.token_count_history}")

        return final_explanation
