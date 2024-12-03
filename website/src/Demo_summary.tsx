import { Box, Typography } from "@mui/material";
import { patientData, PatientName } from "./patientData";
import { Grid2 as Grid } from "@mui/material";
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
  const {
    summary_visit,
    admission_diagnoses,
    acquired_diagnoses,
    medications,
  } = patientData[props.patient];

  return (
    <Grid container spacing={1}>
      <Grid size={12}>
        <Box
          sx={{
            borderRadius: "16px",
            borderLeft: "6px solid #b6e0ff",
            bgcolor: "#f9f9f9",
            mb: 1,
            boxShadow: 3,
          }}
        >
          <Box
            sx={{
              display: "inline-block",
              px: 1,
              py: 0.5,
              borderRadius: "16px 0px 16px 0",
              bgcolor: "#b6e0ff",
              color: "#007bff",
              mb: 1,
              position: "relative",
              left: "-6px",
              top: 0,
            }}
          >
            <Typography variant="h5" textAlign="left" color="#0055b0">
              <b>Visit Summary</b>
            </Typography>
          </Box>
          <Box sx={{ p: 1, mt: -2.5 }}>
            <Typography color="black" sx={{ mt: 1 }}>
              <b>Admission Date:</b> {summary_visit["AdmissionDate"]}
              <br />
              <b>Visit Reason:</b> {summary_visit["visit_reason"]}
              <br />
              <b>Summary:</b> {summary_visit["AdmissionSummary"]}
            </Typography>
          </Box>
        </Box>
      </Grid>

      <Grid size={6}>
        <Box
          sx={{
            borderRadius: "16px",
            borderLeft: "6px solid #ffecb3",
            bgcolor: "#ffffff",
            mb: 1,
            boxShadow: 3,
            height: "250px", // Set a fixed height to match Acquired Diagnoses
            overflowY: "auto", // Enable scrolling if content overflows
          }}
        >
          <Box
            sx={{
              display: "inline-block",
              px: 1,
              py: 0.5,
              borderRadius: "16px 0px 16px 0",
              bgcolor: "#ffecb3",
              color: "#ff8f00",
              mb: 1,
              position: "relative",
              left: "-6px",
              top: 0,
            }}
          >
            <Typography variant="h6" textAlign="left">
              Admission Diagnoses
            </Typography>
          </Box>
          <List>
            {admission_diagnoses.map((diagnosis, index) => (
              <div key={index}>
                <ListItem>
                  <ListItemText
                    primary={
                      diagnosis.condition === "Unspecified"
                        ? "None"
                        : diagnosis.condition
                    }
                    sx={{ color: "black" }}
                  />
                </ListItem>
                {index < admission_diagnoses.length - 1 && <Divider />}
              </div>
            ))}
          </List>
        </Box>
      </Grid>

      <Grid size={6}>
        <Box
          sx={{
            borderRadius: "16px",
            borderLeft: "6px solid #9dc4c9",
            bgcolor: "#ffffff",
            mb: 1,
            boxShadow: 3,
            height: "250px", // Set a fixed height
            overflowY: "auto", // Enable scrolling if content overflows
          }}
        >
          <Box
            sx={{
              display: "inline-block",
              px: 1,
              py: 0.5,
              borderRadius: "16px 0px 16px 0",
              bgcolor: "#9dc4c9",
              color: "#006064",
              mb: 1,
              position: "relative",
              left: "-6px",
              top: 0,
            }}
          >
            <Typography variant="h6" textAlign="left">
              Acquired Diagnoses
            </Typography>
          </Box>
          <List>
            {acquired_diagnoses.map((diagnosis, index) => (
              <div key={index}>
                <ListItem>
                  <ListItemText
                    primary={
                      diagnosis.condition === "Unspecified"
                        ? "None"
                        : diagnosis.condition
                    }
                    sx={{ color: "black" }}
                  />
                </ListItem>
                {index < acquired_diagnoses.length - 1 && <Divider />}
              </div>
            ))}
          </List>
        </Box>
      </Grid>

      {/* Current Medications */}
      <Grid
        size={12}
        sx={{
          overflow: "visible",
        }}
      >
        <Box
          sx={{
            minHeight: "250px", // Ensure enough height for the box
            overflow: "visible", // Prevent clipping
          }}
        >
          <Box
            sx={{
              borderRadius: "16px",
              borderLeft: "6px solid #c8e6c9",
              bgcolor: "#ffffff",
              mt: 1,
              height: "200px",
            }}
          >
            <Box
              sx={{
                display: "inline-block",
                px: 1,
                py: 0.5,
                borderRadius: "16px 0px 16px 0",
                bgcolor: "#c8e6c9",
                color: "#388e3c",
                position: "relative",
                left: "-6px",
                top: 0,
              }}
            >
              <Typography variant="h6" textAlign="left">
                Current Medication
              </Typography>
            </Box>
            <List sx={{ maxHeight: 150, overflowY: "auto", bgcolor: "white" }}>
              {medications.map((medication, index) => (
                <div key={index}>
                  <ListItem>
                    <ListItemText
                      primary={medication.name}
                      secondary={`Dosage: ${medication.dosage}`}
                      sx={{ color: "black" }}
                    />
                    <Tooltip title={medication.reason} placement="top">
                      <IconButton>
                        <InfoIcon />
                      </IconButton>
                    </Tooltip>
                  </ListItem>
                  {index < medications.length - 1 && <Divider />}
                </div>
              ))}
            </List>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
