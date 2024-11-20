import os
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import jwt
import time
import uuid
from cryptography.hazmat.primitives import serialization
from pathlib import Path  # Import Path from pathlib

from dotenv import load_dotenv  # Import load_dotenv

load_dotenv() 

class FHIRConnection:
    def __init__(self):
        # Load environment variables
        self.client_id = os.getenv("FHIR_CLIENT_ID")
        self.private_key_path = Path(os.getenv("FHIR_PRIVATE_KEY_PATH"))
        
        # Check if environment variables are set
        if not self.client_id or not self.private_key_path.exists():
            raise ValueError("Environment variables for FHIR_CLIENT_ID or FHIR_PRIVATE_KEY_PATH are not set correctly.")
        
        self.base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
        self.token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
        self.private_key = self.load_private_key()

    def load_private_key(self):
        with open(self.private_key_path, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)

    def generate_jwt(self):
        issued_at = int(time.time())
        expiration_time = issued_at + 300  # Token valid for 5 minutes
        jti = str(uuid.uuid4())

        payload = {
            "iss": self.client_id,
            "sub": self.client_id,
            "aud": self.token_url,
            "jti": jti,
            "exp": expiration_time,
            "nbf": issued_at,
            "iat": issued_at,
        }

        header = {
            "alg": "RS384",
            "typ": "JWT"
        }

        return jwt.encode(payload, self.private_key, algorithm="RS384", headers=header)

    def get_access_token(self):
        try:
            jwt_assertion = self.generate_jwt()
            data = {
                "grant_type": "client_credentials",
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": jwt_assertion,
            }
            token_response = requests.post(self.token_url, data=data)
            token_response.raise_for_status()  # Raise an error for bad responses
            return token_response.json().get("access_token")
        except requests.RequestException as e:
            print(f"Error fetching access token: {e}")
            return None

    def parse_patient(self, response):
        try:
            root = ET.fromstring(response.text)
            # Define the namespace
            namespace = {'ns': 'http://hl7.org/fhir'}

            # Extract patient details (assuming it's consistent across entries)
            patient_reference = root.find(".//ns:subject/ns:reference", namespace)
            patient_name = root.find(".//ns:subject/ns:display", namespace)

            # Safely get attributes
            patient_reference_value = patient_reference.attrib["value"] if patient_reference is not None else "Unknown"
            patient_name_value = patient_name.attrib["value"] if patient_name is not None else "Unknown"

            # Initialize list to store condition details
            conditions = []

            # Loop through each entry in the Bundle
            for entry in root.findall(".//ns:entry", namespace):
                condition = entry.find(".//ns:Condition", namespace)
                if condition is not None:
                    condition_id = condition.find("ns:id", namespace)
                    condition_id_value = condition_id.attrib["value"] if condition_id is not None else "Unknown"
                    
                    clinical_status = condition.find(".//ns:clinicalStatus/ns:coding/ns:display", namespace)
                    clinical_status_value = clinical_status.attrib["value"] if clinical_status is not None else "Unknown"
                    
                    verification_status = condition.find(".//ns:verificationStatus/ns:coding/ns:display", namespace)
                    verification_status_value = verification_status.attrib["value"] if verification_status is not None else "Unknown"
                    
                    category_elements = condition.findall(".//ns:category", namespace)
                    category = ", ".join(
                        cat.find("ns:coding/ns:display", namespace).attrib["value"]
                        for cat in category_elements if cat.find("ns:coding/ns:display", namespace) is not None
                    )
                    
                    diagnosis_codes = ", ".join(
                        f"{code.attrib['value']} ({code.get('display', {}).get('value', '')})"
                        for code in condition.findall(".//ns:code/ns:coding/ns:code", namespace)
                    )
                    
                    encounter = condition.find(".//ns:encounter/ns:display", namespace)
                    encounter_display = encounter.attrib["value"] if encounter is not None else "N/A"
                    
                    onset_date = condition.find(".//ns:onsetDateTime", namespace)
                    onset_date_value = onset_date.attrib["value"] if onset_date is not None else "N/A"
                    
                    recorded_date = condition.find(".//ns:recordedDate", namespace)
                    recorded_date_value = recorded_date.attrib["value"] if recorded_date is not None else "N/A"
                    
                    # Add condition details to the list
                    conditions.append({
                        "Patient Name": patient_name_value,
                        "Patient Reference": patient_reference_value,
                        "Condition ID": condition_id_value,
                        "Clinical Status": clinical_status_value,
                        "Verification Status": verification_status_value,
                        "Category": category,
                        "Diagnosis Codes": diagnosis_codes,
                        "Encounter": encounter_display,
                        "Onset Date": onset_date_value,
                        "Recorded Date": recorded_date_value,
                    })

            # Aggregate conditions into a single row for the patient
            aggregated_row = {
                "Patient Name": patient_name_value,
                "Patient Reference": patient_reference_value,
                "Conditions": "; ".join(
                    f"ID: {cond['Condition ID']}, Clinical Status: {cond['Clinical Status']}, "
                    f"Verification Status: {cond['Verification Status']}, Category: {cond['Category']}, "
                    f"Codes: {cond['Diagnosis Codes']}, Encounter: {cond['Encounter']}, "
                    f"Onset: {cond['Onset Date']}, Recorded: {cond['Recorded Date']}"
                    for cond in conditions
                )
            }

            final_df = pd.DataFrame([aggregated_row])
            return final_df
        except ET.ParseError as e:
            print(f"Error parsing XML response: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def fetch_patient_conditions(self, patient_id):
        access_token = self.get_access_token()
        if not access_token:
            return pd.DataFrame()  # Return empty DataFrame if token retrieval failed
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        endpoint = f"{self.base_url}/Condition"
        params = {"patient": patient_id}
        response = requests.get(endpoint, headers=headers, params=params)
        return self.parse_patient(response)

# Usage example (to be called from other parts of the project)
# fhir_connection = FHIRConnection()
# df = fhir_connection.fetch_patient_conditions("eq081-VQEgP8drUUqCWzHfw3")

# print(df)



