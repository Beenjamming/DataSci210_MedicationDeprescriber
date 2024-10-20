import donald from "./assets/donald_duck.json";

interface Diagnosis {
  condition: string;
  diagnosed_on: string;
  severity?: string;
  treatment: string;
  resolved?: boolean;
}

interface SummaryVisit {
  AdmissionDate: string;
  visit_reason: string;
  AdmissionSummary: string;
}

interface Medication {
  name: string;
  dosage: string;
  reason: string;
}
interface Notes {
  provider_name: string;
  provider_specialty: string;
  note_type: string;
  note_date: string;
  note_content: string;
}

interface Patient {
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  summary_visit: SummaryVisit;
  current_diagnoses: Diagnosis[];
  past_diagnoses: Diagnosis[];
  medications: Medication[];
  notes: Notes[];
}

export type PatientName = "Donald" | "Mickey";
export const patientData: Record<PatientName, Patient> = {
  Mickey: donald,
  Donald: donald,
};
