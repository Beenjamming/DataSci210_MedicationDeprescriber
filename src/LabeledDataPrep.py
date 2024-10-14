import re

import pandas as pd


# Function to extract surrounding words
def extract_surrounding_text(text, notes_rm_debug=False):
    match = re.search(r"(\S+\s+){0,6}DISCHARGE(\s+\S+){0,6}", text)
    # if match:
    #     print(match.group(0))
    return match.group(0) if match else None


def get_labled_encounters(data_path):
    """
    returns labled encounters df

    """
    labels = pd.read_csv(data_path / "LabeledResponses.csv")
    encounters = pd.read_csv(data_path / "encounters.txt", delimiter="|")

    return encounters.merge(labels, left_on="EncounterKey", right_on="key")


def get_notes(data_path, notes_rm_debug=False):
    """
    returns cleaned notes df

    """

    # labeled encounters df
    le_df = get_labled_encounters(data_path=data_path)

    notes = pd.read_csv(data_path / "noteText.csv")

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
    notes["discharge_text"] = notes["NoteText"].apply(extract_surrounding_text)

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

        rm_notes.to_csv(data_path / "removed_discharged_notes.csv", index=False)

    return notes[notes.discharge_text.isna()]
