import re
from pathlib import Path

import pandas as pd


class DataLoader:
    """Class to handle loading patient data by 'EncourterKey'"""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path

    # exclude encounter keys of patients who died during their stay
    death_encs = [
        "D671A9D60DED51",
        "D1A8A0B77B70E0",
        "DC3EF907D114BE",
        "DCC9687AF26987",
        "D1FE26FC370FFC",
        "D009F2D78A0374",
        "D6B0465FB6D347",
        "D9BC589B1471E4",
        "DE95D7D457CFE2",
        "D45728A2EFD315",
        "DE9B248630A783",
        "D888D223470633",
        "DD52E983718FAC",
        "D74984AD1716DE",
        "D3B195924276E0",
        "D7499004435440",
        "D4327278A34F23",
        "D5A4459EC3D5A3",
        "D5207C914A3189",
        "D03F292AFD16BA",
        "DC5430B22637DD",
        "DE53DA13107A5B",
        "D304C167A23716",
        "D92F213A1469C9",
        "D41B6D4C4712DE",
        "DB3584A13B7E03",
        "DA1B298F51163A",
        "DC319B5B67AC57",
        "DFC887F7797FED",
        "DDC353DAD2BD34",
        "D3E47A655F3331",
        "D1AD6B5B14FB21",
        "D5A348477BA458",
        "DC2966E64CC1D6",
        "D8017C77BA15FA",
        "D22E2C0CC95593",
        "D2F2263CF3CB22",
    ]

    def get_data(self, encounter_key: str) -> dict:
        """Load and return all data."""
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

        # filter all the death encounters out of the data
        if encounter_key in DataLoader.death_encs:
            return None

        data_dict = {
            "noteConcepts": noteConcepts,
            "encounter": encounters,
            "orders": orders,
            "hospitalAcquiredDx": hospitalAcquiredDx,
            "noteText": noteText,
            "presentOnAdmitDx": presentOnAdmitDx,
        }
        return data_dict

    def get_label_df(self):
        """Return a single row with the key, reason and recommendation."""
        return pd.read_csv(self.data_path / "LabeledResponses.csv")

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
        # exclude all death encounters
        if encounter_key in DataLoader.death_encs:
            return None

        return data_dict

    def get_encounter_data(self, encounter_key: str) -> str:
        """Return only encounter data filtered by encounter_key."""

        encounters = pd.read_csv(self.data_path / "encounters.txt", sep="|")

        encounters = encounters[encounters["EncounterKey"] == encounter_key]

        encounters_json = encounters.to_json(orient="records")

        # exclude all death encounters
        if encounter_key in DataLoader.death_encs:
            return None

        return encounters_json

    def get_notes_data(self, encounter_key: str, notes_rm_debug=False):
        """
        returns cleaned notes df

        """

        notes = pd.read_csv(self.data_path / "labled_notes_w_summary.csv")
        notes = notes[notes["EncounterKey"] == encounter_key]
        # order by NoteDate descending
        notes = notes.sort_values(by="NoteDate", ascending=False)
        notes = notes[~notes.llm_summary.str.contains("No diagnoses", na=False)]

        return notes[notes.discharge_text.isna()]

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
