import { patientData, PatientName } from "./patientData";
import { Box, Avatar, Typography, Divider } from "@mui/material";

interface PatientSummaryProps {
  patient: PatientName;
}

export default function PatientInfo(props: PatientSummaryProps) {
  const {
    patient_id,
    name,
    age,
    gender,
    race,
    DOB,
    precautions,
    allergies,
    provider,
  } = patientData[props.patient];
  return (
    <Box height="100vh" sx={{ bgcolor: "#e3f2fd", pt: 1 }}>
      <Box display="flex" flexDirection="column" alignItems="center">
        <Avatar sx={{ bgcolor: "#004c8c", width: 100, height: 100 }}>
          {name
            .split(" ")
            .map((word) => word.charAt(0))
            .join("")}
        </Avatar>
        <Typography variant="h6" color="black">
          <b>{name}</b>
        </Typography>
        <Typography color="black">
          <b>MRN:</b> {patient_id}
          <br />
          <b>Age:</b> {age}
          <br />
          <b>Sex:</b> {gender}
          <br />
          <b>Race:</b> {race}
          <br />
          <b>DOB:</b> {DOB}
        </Typography>
      </Box>
      <Divider
        flexItem
        sx={{ borderColor: "black", borderBottomWidth: 2, mt: 1 }}
      />
      <Box sx={{ m: 1 }}>
        <Typography color="blue">
          <b>Provider Information</b>
        </Typography>
        <Box display="flex" alignItems="center" mt={2}>
          {/* Avatar */}
          <Avatar sx={{ bgcolor: "#8c1f7a", width: 50, height: 50, mr: 2 }}>
            {provider.name
              .split(" ")
              .map((word) => word.charAt(0))
              .join("")}
          </Avatar>
          {/* Information */}
          <Box>
            <Typography color="black">
              <b>{provider.name}</b>
            </Typography>
            <Typography color="black">{provider.provider_specialty}</Typography>
          </Box>
        </Box>
      </Box>
      <Divider
        flexItem
        sx={{ borderColor: "black", borderBottomWidth: 2, mt: 1 }}
      />
      <Box sx={{ m: 1 }}>
        <Typography color="#8c1f7a">
          <b>Precautions</b>
        </Typography>
        <Typography color="black"> {precautions} </Typography>
      </Box>
      <Divider
        flexItem
        sx={{ borderColor: "black", borderBottomWidth: 2, mt: 1 }}
      />
      <Box sx={{ m: 1 }}>
        <Typography color="green">
          <b>Allergies</b>
        </Typography>
        <Typography color="black"> {allergies} </Typography>
      </Box>
    </Box>
  );
}
