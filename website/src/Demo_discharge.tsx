import { useState } from "react";
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
  List,
  ListItem,
  ListItemText,
  ListItemButton,
} from "@mui/material";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import InfoIcon from "@mui/icons-material/Info";
import { patientData, PatientName } from "./patientData";

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

interface Notes {
  id: string;
  provider_name: string;
  note_type: string;
  note_date: string;
  note_content: string;
}

interface PatientOrdersProps {
  patient: PatientName;
}

export default function PatientMedicationDischarge(props: PatientOrdersProps) {
  const { medication_orders, notes } = patientData[props.patient];

  const [infoDialogOpen, setInfoDialogOpen] = useState(false);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [modifyDialogOpen, setModifyDialogOpen] = useState(false);
  const [dialogContent, setDialogContent] = useState<{
    recommendationDiagnosis: string;
    recommendationReason: string;
    relatedNotes: Notes[];
  } | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<Orders | null>(null);
  const [selectedNote, setSelectedNote] = useState<Notes | null>(null);
  const [noteDialogOpen, setNoteDialogOpen] = useState(false);
  const [modifyValue, setModifyValue] = useState("");
  const [localFeedback, setLocalFeedback] = useState({
    like: null as boolean | null,
    text: "",
  });
  const [highlightedButton, setHighlightedButton] = useState<{
    orderName: string;
    action: string;
  } | null>(null);

  const categorizedMeds = medication_orders.reduce(
    (acc, med) => {
      acc[med.category] = acc[med.category] || [];
      acc[med.category].push(med);
      return acc;
    },
    {} as Record<string, Orders[]>,
  );

  const getRelatedNotes = (relatedNoteIds: string[]): Notes[] => {
    return notes.filter((note) => relatedNoteIds.includes(note.id));
  };

  const handleInfoButtonClick = (
    recommendationDiagnosis: string,
    recommendationReason: string,
    relatedNoteIds: string[] = [],
  ) => {
    const relatedNotes = getRelatedNotes(relatedNoteIds);
    setDialogContent({
      recommendationDiagnosis,
      recommendationReason,
      relatedNotes,
    });
    setInfoDialogOpen(true);
  };

  const handleDialogClose = () => {
    setInfoDialogOpen(false);
    setDialogContent(null);
  };

  const handleModifyClick = (order: Orders) => {
    setSelectedOrder(order);
    setModifyValue(order.dose || "");
    setHighlightedButton({ orderName: order.name, action: "modify" });
    setModifyDialogOpen(true);
  };

  const handleModifySubmit = () => {
    console.log("Modified value for:", selectedOrder?.name, modifyValue);
    setModifyDialogOpen(false);
  };

  const handleModifyClose = () => {
    setModifyDialogOpen(false);
    setSelectedOrder(null);
    setModifyValue("");
  };

  const handleFeedbackClick = (order: Orders) => {
    setSelectedOrder(order);
    setFeedbackDialogOpen(true);
  };

  const handleFeedbackClose = () => {
    setFeedbackDialogOpen(false);
    setSelectedOrder(null);
    setLocalFeedback({ like: null, text: "" });
  };

  const handleActionClick = (order: Orders, action: string) => {
    console.log(`${action} action for:`, order.name);
    setHighlightedButton({ orderName: order.name, action });
  };

  const handleNoteClick = (note: Notes) => {
    setSelectedNote(note);
    setNoteDialogOpen(true);
  };

  const handleNoteDialogClose = () => {
    setNoteDialogOpen(false);
    setSelectedNote(null);
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
                key={med.name}
                sx={{ mb: 2, backgroundColor: "rgba(255,255,255,0.5)" }}
              >
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle1">
                        <b>{med.name}</b> ({med.dose})
                      </Typography>
                      <Typography variant="body2">
                        Indication: {med.indication}
                      </Typography>
                      <Typography variant="body2">
                        <b>Status:</b>{" "}
                        {med.ongoing_at_discharge ? "Ongoing" : "Stopped"}
                      </Typography>
                    </Box>
                    <Box
                      sx={{ display: "flex", flexDirection: "column", gap: 1 }}
                    >
                      <Box sx={{ display: "flex", gap: 1 }}>
                        <Button
                          variant="outlined"
                          onClick={() => handleModifyClick(med)}
                          sx={{
                            backgroundColor:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "modify"
                                ? "#FFD700"
                                : "rgba(255, 223, 0, 0.1)",
                            color:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "modify"
                                ? "white"
                                : "black",
                            "&:hover": {
                              backgroundColor: "#FFC107", // Slightly darker yellow
                              color: "white",
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
                                ? "#4CAF50" // Darker green for highlight
                                : "rgba(76, 175, 80, 0.1)", // Light pastel green
                            color:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "resume"
                                ? "white"
                                : "black",
                            "&:hover": {
                              backgroundColor: "#388E3C", // Slightly darker green
                              color: "white",
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
                                ? "#F44336" // Darker red for highlight
                                : "rgba(244, 67, 54, 0.1)", // Light pastel red
                            color:
                              highlightedButton?.orderName === med.name &&
                              highlightedButton.action === "stop"
                                ? "white"
                                : "black",
                            "&:hover": {
                              backgroundColor: "#D32F2F", // Slightly darker red
                              color: "white",
                            },
                          }}
                        >
                          Stop Taking
                        </Button>
                      </Box>
                      {med.recommendation && (
                        <Box display="flex" alignItems="center">
                          <Typography
                            variant="body2"
                            color="#AF1740"
                            sx={{ mt: 1 }}
                          >
                            <b>Recommendation:</b> {med.recommendation}
                          </Typography>
                          {med.recommendation_diagnosis && (
                            <IconButton
                              onClick={() =>
                                handleInfoButtonClick(
                                  med.recommendation_diagnosis || "",
                                  med.recommendation_reason || "",
                                  med.related_notes_ids,
                                )
                              }
                              aria-label="More info"
                              sx={{ ml: 1 }}
                            >
                              <InfoIcon color="primary" />
                            </IconButton>
                          )}
                        </Box>
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

      {/* Info Dialog */}
      <Dialog
        open={infoDialogOpen}
        onClose={handleDialogClose}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>
          <b>Recommendation Details</b>
        </DialogTitle>
        <DialogContent>
          {dialogContent && (
            <>
              <Typography variant="h6">
                <b>Detected Diagnosis:</b>
              </Typography>
              <Typography gutterBottom>
                {dialogContent.recommendationDiagnosis}
              </Typography>
              <Typography variant="h6">
                <b>Recommendation Reasoning:</b>
              </Typography>
              <Typography gutterBottom>
                {dialogContent.recommendationReason}
              </Typography>

              {dialogContent.relatedNotes.length > 0 && (
                <>
                  <Typography variant="h6" gutterBottom>
                    <b>Related Notes:</b>
                  </Typography>
                  <List>
                    {dialogContent.relatedNotes.map((note) => (
                      <ListItem
                        key={note.id}
                        component="div"
                        onClick={() => handleNoteClick(note)}
                        sx={{
                          backgroundColor: "#f7f9fc",
                          borderRadius: "5px",
                          marginBottom: "10px",
                          border: "1px solid #ddd",
                          "&:hover": {
                            backgroundColor: "#e6f7ff",
                            cursor: "pointer",
                          },
                        }}
                      >
                        <ListItemButton>
                          <ListItemText
                            primary={`${note.provider_name} - ${note.note_type}`}
                            secondary={`Date: ${note.note_date}`}
                          />
                        </ListItemButton>
                      </ListItem>
                    ))}
                  </List>
                </>
              )}
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleDialogClose}
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

      {/* Feedback Dialog */}
      <Dialog
        open={feedbackDialogOpen}
        onClose={handleFeedbackClose}
        fullWidth
        maxWidth="sm"
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
              onClick={() =>
                setLocalFeedback((prev) => ({
                  ...prev,
                  like: prev.like === true ? null : true, // Toggle thumbs up
                }))
              }
              color={localFeedback.like === true ? "primary" : "default"}
            >
              <ThumbUpIcon />
            </IconButton>
            <IconButton
              onClick={() =>
                setLocalFeedback((prev) => ({
                  ...prev,
                  like: prev.like === false ? null : false, // Toggle thumbs down
                }))
              }
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
            onChange={(e) =>
              setLocalFeedback((prev) => ({ ...prev, text: e.target.value }))
            }
          />
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleFeedbackClose}
            color="primary"
            variant="contained"
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Note Content Dialog */}
      <Dialog
        open={noteDialogOpen}
        onClose={handleNoteDialogClose}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Note Details</DialogTitle>
        <DialogContent>
          {selectedNote && (
            <>
              <Typography variant="h6" gutterBottom>
                {selectedNote.provider_name} - {selectedNote.note_type}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Date: {selectedNote.note_date}
              </Typography>
              <Typography
                variant="body1"
                dangerouslySetInnerHTML={{ __html: selectedNote.note_content }}
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleNoteDialogClose}
            color="primary"
            variant="contained"
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
