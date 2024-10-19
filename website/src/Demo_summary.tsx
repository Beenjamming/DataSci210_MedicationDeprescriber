import React from "react";
import { Box, Typography } from "@mui/material";
import { patientData, PatientName } from "./patientData";
import Card from "@mui/material/Card";

interface PatientSummaryProps {
  patient: PatientName;
}
export default function PatientSummary(props: PatientSummaryProps) {
  const { summary_visit, current_diagnoses, past_diagnoses } =
    patientData[props.patient];
  return (
    <Box>
      <Card variant="outlined" sx={{ p: 2 }}>
        <Typography variant="h5" textAlign="center">
          <b>Visit Summary</b>
        </Typography>
        <Typography color="black">
          <b>Admission Date:</b> {summary_visit["AdmissionDate"]}
          <br></br>
          <b>Visit Reason:</b> {summary_visit["visit_reason"]}
          <br></br>
          <b>Summary: </b>
          {summary_visit["AdmissionSummary"]}
        </Typography>
      </Card>
    </Box>
  );
}
