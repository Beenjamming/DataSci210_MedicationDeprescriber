import numpy as np
import pandas as pd
import json
import re
from pathlib import Path


class DataLoader:
    """Class to handle loading data by 'EncourterKey'"""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path

    def get_data(self, encounter_key: str) -> dict:
        """ """
        noteConcepts = pd.read_csv(self.data_path / "noteConcepts.txt", sep="|")
        encounters = pd.read_csv(self.data_path / "encounters.txt", sep="|")
        orders = pd.read_csv(self.data_path / "orders.txt", sep="|")
        hospitalAcquiredDx = pd.read_csv(
            self.data_path / "hospitalAcquiredDx.txt", sep="|"
        )
        noteText = pd.read_csv(self.data_path / "noteText.txt", sep="|")
        presentOnAdmitDx = pd.read_csv(self.data_path / "presentOnAdmitDx.txt", sep="|")

        # filter all dfs to the selected encounter_key
        noteConcepts = noteConcepts[noteConcepts["EncounterKey"] == encounter_key]
        encounters = encounters[encounters["EncounterKey"] == encounter_key]
        orders = orders[orders["EncounterKey"] == encounter_key]
        hospitalAcquiredDx = hospitalAcquiredDx[
            hospitalAcquiredDx["EncounterKey"] == encounter_key
        ]
        noteText = noteText[noteText["EncounterKey"] == encounter_key]
        presentOnAdmitDx = presentOnAdmitDx[
            presentOnAdmitDx["EncounterKey"] == encounter_key
        ]

        data_dict = {
            "noteConcepts": noteConcepts,
            "encounter": encounters,
            "orders": orders,
            "hospitalAcquiredDx": hospitalAcquiredDx,
            "noteText": noteText,
            "presentOnAdmitDx": presentOnAdmitDx,
        }
        return data_dict

    def get_label(self, encounter_key: str) -> str:
        """ """
        labels_df = pd.read_csv(self.data_path / "LabeledResponses.csv")
        return labels_df  # [labels_df["key"] == encounter_key]

    def get_diagnosis_data(self, encounter_key: str) -> dict:
        """Return only diagnosis data filtered by encounter_key."""
        hospitalAcquiredDx = pd.read_csv(
            self.data_path / "hospitalAcquiredDx.txt", sep="|"
        )
        presentOnAdmitDx = pd.read_csv(self.data_path / "presentOnAdmitDx.txt", sep="|")

        hospitalAcquiredDx = hospitalAcquiredDx[
            hospitalAcquiredDx["EncounterKey"] == encounter_key
        ]
        presentOnAdmitDx = presentOnAdmitDx[
            presentOnAdmitDx["EncounterKey"] == encounter_key
        ]

        hospitalAcquiredDx_json = hospitalAcquiredDx.to_json(orient="records")
        presentOnAdmitDx_json = presentOnAdmitDx.to_json(orient="records")

        data_dict = {
            "hospitalAcquiredDx": hospitalAcquiredDx_json,
            "presentOnAdmitDx": presentOnAdmitDx_json,
        }

        return data_dict

    def get_encounter_data(self, encounter_key: str) -> json:
        """Return only encounter data filtered by encounter_key."""

        encounters = pd.read_csv(self.data_path / "encounters.txt", sep="|")

        encounters = encounters[encounters["EncounterKey"] == encounter_key]

        encounters_json = encounters.to_json(orient="records")

        return encounters_json

    @staticmethod
    def extract_surrounding_text(text, notes_rm_debug=False):
        match = re.search(r"(\S+\s+){0,6}DISCHARGE(\s+\S+){0,6}", text)
        # if match:
        #     print(match.group(0))
        return match.group(0) if match else None

    def get_labled_encounters(self):
        """
        returns labled encounters df

        """
        labels = pd.read_csv(self.data_path / "LabeledResponses.csv")
        encounters = pd.read_csv(self.data_path / "encounters.txt", delimiter="|")

        return encounters.merge(labels, left_on="EncounterKey", right_on="key")

    def get_notes_data(self, encounter_key: str, notes_rm_debug=False):
        """
        returns cleaned notes df

        """

        # labeled encounters df
        le_df = self.get_labled_encounters()

        notes = pd.read_csv(self.data_path / "noteText.csv")

        # Step 1: Find the maximum NoteDate for each EncounterKey
        max_note_date = notes.groupby("EncounterKey")["NoteDate"].transform("max")
        # Step 2: Create a binary column indicating if it's the latest note for that encounter

        notes["is_on_last_note_date"] = (notes["NoteDate"] == max_note_date).astype(int)

        notes = notes.merge(
            le_df[["key", "PtDischargeDate"]], left_on="EncounterKey", right_on="key"
        )

        selected_providers = [
            "Resident",
            "Physician",
            "Registered Nurse",
            "Nurse Practitioner",
            "Physician Assistant",
            "Pharmacist",
            "Licensed Vocational Nurse",
            "Medical Student",
            "Pharmacy Student",
            "Nursing Student",
            "Registered Dietitian",
            "Dietetic Intern",
        ]
        notes = notes[
            (notes["ProviderType"].isin(selected_providers))
            | (notes["ProviderType"].isnull())
        ]

        # Apply the function to the text column
        notes["discharge_text"] = notes["NoteText"].apply(
            DataLoader.extract_surrounding_text
        )

        if notes_rm_debug:
            # REMOVED these Notes
            rm_notes = notes[~notes.discharge_text.isna()]
            rm_notes["PtDischargeDate"] = pd.to_datetime(
                rm_notes["PtDischargeDate"], errors="coerce"
            )
            rm_notes["NoteDate"] = pd.to_datetime(rm_notes["NoteDate"], errors="coerce")

            # Calculate the difference while handling missing values
            rm_notes["dis-note_vs_dis-date"] = (
                rm_notes["PtDischargeDate"] - rm_notes["NoteDate"]
            )

            rm_notes.to_csv(
                self.data_path / "removed_discharged_notes.csv", index=False
            )

        notes = notes[notes["EncounterKey"] == encounter_key]

        return notes[notes.discharge_text.isna()]
