import React from "react";
import { patientData, PatientName } from "./patientData";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
} from "@mui/material";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";

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
  recommendation_notes?: string[];
}

interface PatientOrdersProps {
  patient: PatientName;
}

export default function PatientMedicationDischarge(props: PatientOrdersProps) {
  const { medication_orders } = patientData[props.patient];

  const [feedbackDialogOpen, setFeedbackDialogOpen] = React.useState(false);
  const [modifyDialogOpen, setModifyDialogOpen] = React.useState(false);
  const [selectedOrder, setSelectedOrder] = React.useState<Orders | null>(null);
  const [localFeedback, setLocalFeedback] = React.useState({
    like: null as boolean | null,
    text: "",
  });
  const [modifyValue, setModifyValue] = React.useState("");
  const [highlightedButton, setHighlightedButton] = React.useState<{
    orderName: string;
    action: string;
  } | null>(null);

  // Group medications by category
  const categorizedMeds = medication_orders.reduce(
    (acc, med) => {
      acc[med.category] = acc[med.category] || [];
      acc[med.category].push(med);
      return acc;
    },
    {} as Record<string, Orders[]>,
  );

  const handleFeedbackClick = (order: Orders) => {
    setSelectedOrder(order);
    setFeedbackDialogOpen(true);
  };

  const handleFeedbackClose = () => {
    setFeedbackDialogOpen(false);
    setSelectedOrder(null);
    setLocalFeedback({ like: null, text: "" });
  };

  const handleModifyClick = (order: Orders) => {
    setSelectedOrder(order);
    setModifyValue(order.dose || ""); // Pre-fill with the current value
    setModifyDialogOpen(true);
  };

  const handleModifyClose = () => {
    setModifyDialogOpen(false);
    setSelectedOrder(null);
    setModifyValue("");
  };

  const handleModifySubmit = () => {
    if (selectedOrder) {
      console.log("Modified value for:", selectedOrder.name, modifyValue);
    }
    setModifyDialogOpen(false);
  };

  const handleActionClick = (order: Orders, action: string) => {
    console.log(`${action} action for:`, order.name);
    setHighlightedButton({ orderName: order.name, action });
  };

  const handleThumbClick = (like: boolean) => {
    setLocalFeedback((prev) => ({ ...prev, like }));
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalFeedback((prev) => ({ ...prev, text: e.target.value }));
  };

  return (
    <Box>
      <Typography variant="h4" color="black" gutterBottom>
        Discharge Medication
      </Typography>

      <Box
        sx={{
          p: 4,
          maxHeight: 700,
          overflowY: "auto",
          borderRadius: 2,
        }}
      >
        {Object.entries(categorizedMeds).map(([category, meds]) => (
          <Box key={category} sx={{ mb: 4 }}>
            <Typography variant="h6" color="primary" gutterBottom>
              {category}
            </Typography>
            {meds.map((med) => (
              <Card
                key={`${med.name}-${med.date_ordered}`}
                sx={{
                  mb: 2,
                  backgroundColor: "rgba(255,255,255,0.5)",
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    {/* Left Section: Medication Details */}
                    <Box>
                      <Typography variant="subtitle1">
                        <b>{med.name}</b> ({med.dose})
                      </Typography>
                      <Typography variant="body2">
                        Indication: {med.indication}
                      </Typography>
                      <Typography variant="body2">
                        <b>Status: </b>{" "}
                        {med.ongoing_at_discharge ? "Ongoing" : "Stopped"}
                      </Typography>
                    </Box>

                    {/* Right Section: Buttons */}
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "flex-end",
                        gap: 1,
                      }}
                    >
                      <Box
                        sx={{
                          display: "flex",
                          flexDirection: "row",
                          gap: 1,
                        }}
                      >
                        <Button
                          variant="outlined"
                          onClick={() => handleModifyClick(med)}
                          sx={{
                            backgroundColor:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "modify"
                                ? "#62acfc"
                                : "transparent",
                            borderColor: "primary.main",
                            "&:hover": {
                              backgroundColor: "#69a3f5",
                            },
                          }}
                        >
                          Modify
                        </Button>
                        <Button
                          variant="outlined"
                          onClick={() => handleActionClick(med, "resume")}
                          sx={{
                            backgroundColor:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "resume"
                                ? "#62acfc"
                                : "transparent",
                            borderColor: "success.main",
                            "&:hover": {
                              backgroundColor: "#69a3f5",
                            },
                          }}
                        >
                          Resume
                        </Button>
                        <Button
                          variant="outlined"
                          onClick={() => handleActionClick(med, "stop")}
                          sx={{
                            backgroundColor:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "stop"
                                ? "#fc838e"
                                : "transparent",
                            borderColor: "error.main",
                            "&:hover": {
                              backgroundColor: "#F5C2C7",
                            },
                          }}
                        >
                          Stop Taking
                        </Button>
                      </Box>
                      {med.recommendation && (
                        <Typography
                          variant="body2"
                          color="#AF1740"
                          sx={{ mt: 1 }}
                        >
                          <b>Recommendation: </b> {med.recommendation}
                        </Typography>
                      )}
                      {med.recommendation && (
                        <Button
                          variant="outlined"
                          onClick={() => handleFeedbackClick(med)}
                        >
                          Provide Feedback
                        </Button>
                      )}
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        ))}
      </Box>

      {/* Feedback Dialog */}
      <Dialog
        open={feedbackDialogOpen}
        onClose={handleFeedbackClose}
        fullWidth
        maxWidth="sm"
        PaperProps={{
          sx: { backgroundColor: "white" }, // Cream color
        }}
      >
        <DialogTitle>
          {selectedOrder?.name} ({selectedOrder?.dose})
        </DialogTitle>
        <DialogContent>
          <Box
            display="flex"
            alignItems="center"
            justifyContent="center"
            mb={3}
          >
            <Typography variant="body1" sx={{ mr: 2 }}>
              Was this recommendation helpful?
            </Typography>
            <IconButton
              onClick={() => handleThumbClick(true)}
              color={localFeedback.like === true ? "primary" : "default"}
            >
              <ThumbUpIcon />
            </IconButton>
            <IconButton
              onClick={() => handleThumbClick(false)}
              color={localFeedback.like === false ? "error" : "default"}
            >
              <ThumbDownIcon />
            </IconButton>
          </Box>
          <Typography variant="body2" mb={1}>
            Additional Feedback:
          </Typography>
          <TextField
            multiline
            fullWidth
            rows={3}
            value={localFeedback.text}
            onChange={handleTextChange}
          />
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => handleFeedbackClose()}
            color="primary"
            variant="contained"
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modify Dialog */}
      <Dialog
        open={modifyDialogOpen}
        onClose={handleModifyClose}
        fullWidth
        maxWidth="sm"
        PaperProps={{
          sx: { backgroundColor: "white" }, // Cream color
        }}
      >
        <DialogTitle>Modify Medication</DialogTitle>
        <DialogContent>
          <Typography variant="body2" mb={1}>
            Adjust dosage for <b>{selectedOrder?.name}</b> (
            {selectedOrder?.dose})
          </Typography>
          <TextField
            fullWidth
            value={modifyValue}
            onChange={(e) => setModifyValue(e.target.value)}
            placeholder="Enter new value"
          />
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleModifySubmit}
            color="primary"
            variant="contained"
          >
            Save
          </Button>
          <Button
            onClick={handleModifyClose}
            color="secondary"
            variant="outlined"
          >
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
