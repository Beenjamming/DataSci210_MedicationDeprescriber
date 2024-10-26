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

interface Orders {
  medication_name: string;
  category: string;
  dose: string;
  route: string;
  frequency: string;
  indication: string;
  status: string;
  date_ordered: string;
  date_start: string;
  date_end: string;
  is_ongoing_for_discharge: boolean;
  recommendation?: string;
  recommendation_notes?: string[];
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
  medication_orders: Orders[];
}

export type PatientName = "Donald" | "Mickey";
export const patientData: Record<PatientName, Patient> = {
  Mickey: donald,
  Donald: donald,
};
