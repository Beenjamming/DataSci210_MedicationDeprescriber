import { patientData, PatientName } from "./patientData";
import { Box, Avatar, Typography, Divider } from "@mui/material";

interface PatientSummaryProps {
  patient: PatientName;
}

export default function PatientInfo(props: PatientSummaryProps) {
  const { patient_id, name, age, gender, race } = patientData[props.patient];
  return (
    <Box height="100vh" sx={{ bgcolor: "#9ad1d4", pt: 1 }}>
      <Box display="flex" flexDirection="column" alignItems="center">
        <Avatar sx={{ bgcolor: "primary.main", width: 100, height: 100 }}>
          {name.charAt(0)}
        </Avatar>
        <Typography variant="h6" color="black">
          <b>{name}</b>
        </Typography>
        <Typography variant="body1" color="#333333">
          <b>MRN:</b> {patient_id}
        </Typography>
        <Typography color="black">
          <b>Age:</b> {age}
          <br />
          <b>Sex:</b> {gender}
          <br />
          <b>Race:</b> {race}
        </Typography>
      </Box>
      <Divider
        flexItem
        sx={{ borderColor: "black", borderBottomWidth: 2, mt: 1 }}
      />
      <Box sx={{ m: 1 }}>
        <Typography color="#8c1f7a">
          <b>Precautions</b>
        </Typography>
        <Typography color="black">Fall precautions</Typography>
      </Box>
    </Box>
  );
}
