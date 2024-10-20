import { Box, Typography } from "@mui/material";
import { patientData, PatientName } from "./patientData";
import { Grid2 as Grid } from "@mui/material";
import Card from "@mui/material/Card";
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";
import InfoIcon from "@mui/icons-material/Info";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";

interface PatientSummaryProps {
  patient: PatientName;
}

export default function PatientSummary(props: PatientSummaryProps) {
  const { summary_visit, current_diagnoses, past_diagnoses, medications } =
    patientData[props.patient];
  return (
    <Grid container spacing={1}>
      <Grid size={12}>
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
      </Grid>
      <Grid size={6}>
        <Box sx={{ p: 2, bgcolor: "white" }}>
          <Typography variant="h6" textAlign="center" color="black">
            <b>Current Diagnoses</b>
          </Typography>
          <List>
            {current_diagnoses.map((diagnosis, index) => (
              <div key={index}>
                <ListItem>
                  <ListItemText
                    primary={diagnosis.condition}
                    secondary={`Diagnosed On: ${diagnosis.diagnosed_on}`}
                    sx={{ color: "Black" }}
                  />
                  <Tooltip title={diagnosis.treatment} placement="top">
                    <IconButton>
                      <InfoIcon />
                    </IconButton>
                  </Tooltip>
                </ListItem>
                {index < current_diagnoses.length - 1 && <Divider />}
              </div>
            ))}
          </List>
        </Box>
      </Grid>
      <Grid size={6}>
        <Box sx={{ p: 2, bgcolor: "white" }}>
          <Typography variant="h6" textAlign="center" color="black">
            <b>Past Diagnoses</b>
          </Typography>
          <List>
            {past_diagnoses.map((diagnosis, index) => (
              <div key={index}>
                <ListItem>
                  <ListItemText
                    primary={diagnosis.condition}
                    secondary={`Diagnosed On: ${diagnosis.diagnosed_on}`}
                    sx={{ color: "Black" }}
                  />
                  <Tooltip title={diagnosis.treatment} placement="top">
                    <IconButton>
                      <InfoIcon />
                    </IconButton>
                  </Tooltip>
                </ListItem>
                {index < past_diagnoses.length - 1 && <Divider />}
              </div>
            ))}
          </List>
        </Box>
      </Grid>
      <Grid size={12}>
        <Box sx={{ p: 2, bgcolor: "white" }}>
          <Typography variant="h6" textAlign="center" color="black">
            <b>Current Medication</b>
          </Typography>
          <List sx={{ maxHeight: 300, overflow: "auto", bgcolor: "white" }}>
            {medications.map((medication, index) => (
              <div key={index}>
                <ListItem>
                  <ListItemText
                    primary={medication.name}
                    secondary={`Dosage: ${medication.dosage}`}
                    sx={{ color: "Black" }}
                  />
                  <Tooltip title={medication.reason} placement="top">
                    <IconButton>
                      <InfoIcon />
                    </IconButton>
                  </Tooltip>
                </ListItem>
                {index < past_diagnoses.length - 1 && <Divider />}
              </div>
            ))}
          </List>
        </Box>
      </Grid>
    </Grid>
  );
}
