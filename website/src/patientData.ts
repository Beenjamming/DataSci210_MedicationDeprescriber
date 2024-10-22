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

interface Patient {
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  summary_visit: SummaryVisit;
  current_diagnoses: Diagnosis[];
  past_diagnoses: Diagnosis[];
}

export type PatientName = "Donald" | "Mickey";
export const patientData: Record<PatientName, Patient> = {
  Mickey: donald,
  Donald: donald,
};
