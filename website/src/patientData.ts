import donny from "./assets/patient_json/donny_dunlap.json";
import drew from "./assets/patient_json/drew_buck.json";
import melinda from "./assets/patient_json/melinda_scott.json";
import shelton from "./assets/patient_json/shelton_park.json";
import sydney from "./assets/patient_json/sydney_byrd.json";
import willow from "./assets/patient_json/willow_harper.json";

interface Diagnosis {
  condition: string;
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
  id: string;
  provider_name: string;
  provider_specialty: string;
  note_type: string;
  note_date: string;
  note_content: string;
}

interface Orders {
  name: string;
  category: string;
  dose: string;
  route: string;
  frequency: string;
  indication: string;
  status: string;
  date_ordered: string;
  date_start: string;
  date_end: string | null;
  ongoing_at_discharge: boolean;
  recommendation?: string;
  recommendation_diagnosis?: string;
  recommendation_reason?: string;
  related_notes_ids?: string[];
}

interface Provider {
  name: string;
  provider_specialty: string;
}

interface Patient {
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  race: string;
  DOB: string;
  precautions: string;
  provider: Provider;
  allergies: string;
  summary_visit: SummaryVisit;
  admission_diagnoses: Diagnosis[];
  acquired_diagnoses: Diagnosis[];
  medications: Medication[];
  notes: Notes[];
  medication_orders: Orders[];
}

export type PatientName =
  | "Donny Dunlap"
  | "Drew Buck"
  | "Melinda Scott"
  | "Shelton Park"
  | "Sydney Byrd"
  | "Willow Harper";
export const patientData: Record<PatientName, Patient> = {
  "Donny Dunlap": donny,
  "Drew Buck": drew,
  "Melinda Scott": melinda,
  "Shelton Park": shelton,
  "Sydney Byrd": sydney,
  "Willow Harper": willow,
};
