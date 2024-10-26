import React from "react";
import { patientData, PatientName } from "./patientData";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid2 as Grid,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

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

interface PatientOrdersProps {
  patient: PatientName;
}
export default function PatientMedicationDischarge(props: PatientOrdersProps) {
  const { medication_orders } = patientData[props.patient];

  const [openDialog, setOpenDialog] = React.useState(false);
  const [dialogNotes, setDialogNotes] = React.useState<string[] | null>(null);

  const handleInfoClick = (notes: string[]) => {
    setDialogNotes(notes);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setDialogNotes(null);
  };

  const ongoingMeds = medication_orders.filter(
    (med) => med.is_ongoing_for_discharge,
  );
  const nonOngoingMeds = medication_orders.filter(
    (med) => !med.is_ongoing_for_discharge,
  );

  const groupByCategory = (medications: Orders[]) => {
    return medications.reduce(
      (acc, med) => {
        if (!acc[med.category]) acc[med.category] = [];
        acc[med.category].push(med);
        return acc;
      },
      {} as { [key: string]: Orders[] },
    );
  };

  const ongoingCategories = groupByCategory(ongoingMeds);
  const nonOngoingCategories = groupByCategory(nonOngoingMeds);

  return (
    <Box>
      <Box>
        <Typography variant="h4" color="black" gutterBottom>
          Discharge Medication
        </Typography>
      </Box>

      <Box
        sx={{
          p: 4,
          maxHeight: 700,
          overflowY: "auto",
          border: "1px solid black",
          borderRadius: 2,
        }}
      >
        <Box>
          {Object.keys(nonOngoingCategories).map((category) => (
            <Box key={category} sx={{ mb: 3 }}>
              <Typography variant="h6">{category}</Typography>
              {nonOngoingCategories[category].map((med) => (
                <Card
                  key={`${med.medication_name}-${med.date_ordered}`}
                  sx={{ mb: 2, backgroundColor: "rgba(255,255,255,0.5)" }}
                >
                  <CardContent>
                    <Typography variant="subtitle1">
                      <b>{med.medication_name}</b> ({med.dose})
                    </Typography>
                    <Typography variant="body2">
                      Indication: {med.indication}
                    </Typography>
                    <Typography variant="body2">
                      <b>Status: </b>{" "}
                      {med.is_ongoing_for_discharge ? "Ongoing" : "Stopped"}
                    </Typography>
                    {med.recommendation && (
                      <Box display="flex" alignItems="center" sx={{ mt: 1 }}>
                        <Typography variant="body2" color="#AF1740">
                          <b>Recommendation: </b> {med.recommendation}
                        </Typography>
                        {med.recommendation_notes && (
                          <IconButton
                            aria-label="info"
                            onClick={() =>
                              handleInfoClick(med.recommendation_notes || [])
                            }
                            size="small"
                            sx={{ ml: 1 }}
                          >
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        )}
                      </Box>
                    )}
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                      <Grid>
                        <Button variant="contained" color="primary">
                          Modify and Refill
                        </Button>
                      </Grid>
                      <Grid>
                        <Button variant="contained" color="secondary">
                          Resume
                        </Button>
                      </Grid>
                      <Grid>
                        <Button variant="outlined" color="error">
                          Stop Taking
                        </Button>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Box>
          ))}
        </Box>

        <Box>
          {Object.keys(ongoingCategories).map((category) => (
            <Box key={category} sx={{ mb: 3 }}>
              <Typography variant="h6">{category}</Typography>
              {ongoingCategories[category].map((med) => (
                <Card
                  key={`${med.medication_name}-${med.date_ordered}`}
                  sx={{ mb: 2, backgroundColor: "rgba(255,255,255,0.5)" }}
                >
                  <CardContent>
                    <Typography variant="subtitle1">
                      <b>{med.medication_name}</b> ({med.dose})
                    </Typography>
                    <Typography variant="body2">
                      Indication: {med.indication}
                    </Typography>
                    <Typography variant="body2">
                      <b>Status: </b>{" "}
                      {med.is_ongoing_for_discharge ? "Ongoing" : "Stopped"}
                    </Typography>
                    {med.recommendation && (
                      <Box display="flex" alignItems="center" sx={{ mt: 1 }}>
                        <Typography variant="body2" color="#AF1740">
                          <b>Recommendation: </b> {med.recommendation}
                        </Typography>
                        {med.recommendation_notes && (
                          <IconButton
                            aria-label="info"
                            onClick={() =>
                              handleInfoClick(med.recommendation_notes || [])
                            }
                            size="small"
                            sx={{ ml: 1 }}
                          >
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        )}
                      </Box>
                    )}
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                      <Grid>
                        <Button variant="contained" color="primary">
                          Modify
                        </Button>
                      </Grid>
                      <Grid>
                        <Button variant="contained" color="secondary">
                          Prescribe
                        </Button>
                      </Grid>
                      <Grid>
                        <Button variant="outlined" color="error">
                          Don't Prescribe
                        </Button>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Box>
          ))}
        </Box>

        {/* Dialog for Recommendation Notes */}
        <Dialog open={openDialog} onClose={handleCloseDialog}>
          <DialogTitle>Recommendation Notes</DialogTitle>
          <DialogContent>
            {dialogNotes?.map((note, index) => (
              <DialogContentText key={index}>- {note}</DialogContentText>
            ))}
          </DialogContent>
        </Dialog>
      </Box>
    </Box>
  );
}
