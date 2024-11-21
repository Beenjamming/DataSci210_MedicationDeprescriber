import { useState } from "react";
import {
  Divider,
  Grid2 as Grid,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Avatar,
  Button,
  ButtonGroup,
} from "@mui/material";
import { patientData, PatientName } from "./patientData";

interface PatientNotesProps {
  patient: PatientName;
}

export default function PatientNotes(props: PatientNotesProps) {
  const { notes } = patientData[props.patient];
  const [selectedNote, setSelectedNote] = useState(notes[0]);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc" | null>(
    null,
  ); // Sorting direction
  type Notes = {
    note_date: string;
    provider_name: string;
    note_type: string;
    // Add other properties if needed
  };

  const [sortBy, setSortBy] = useState<keyof Notes | null>(null);

  const sortedNotes = [...notes].sort((a, b) => {
    if (!sortBy || !sortDirection) return 0;
    const valueA = a[sortBy];
    const valueB = b[sortBy];
    if (sortDirection === "asc") {
      return valueA > valueB ? 1 : -1;
    }
    if (sortDirection === "desc") {
      return valueA < valueB ? 1 : -1;
    }
    return 0;
  });

  // Handle note click
  const handleNoteClick = (note: (typeof notes)[0]) => {
    setSelectedNote(note);
  };

  return (
    <Grid container spacing={2}>
      <Grid size={4}>
        <Box>
          {/* Sorting Buttons */}
          <Typography variant="subtitle1" color="black" gutterBottom>
            Sort By:
          </Typography>
          <Box
            sx={{
              mb: 1,
              backgroundColor: "white",
              borderRadius: "5px", // Rounded corners
              border: "1px solid #ddd", // Border
            }}
          >
            <ButtonGroup variant="outlined" fullWidth>
              <Button
                onClick={() => {
                  setSortBy("note_date");
                  setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
                }}
              >
                Date{" "}
                {sortBy === "note_date" &&
                  (sortDirection === "asc" ? "↑" : "↓")}
              </Button>
              <Button
                onClick={() => {
                  setSortBy("provider_name");
                  setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
                }}
              >
                Provider{" "}
                {sortBy === "provider_name" &&
                  (sortDirection === "asc" ? "↑" : "↓")}
              </Button>
              <Button
                onClick={() => {
                  setSortBy("note_type");
                  setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
                }}
              >
                Note Type{" "}
                {sortBy === "note_type" &&
                  (sortDirection === "asc" ? "↑" : "↓")}
              </Button>
              <Button
                onClick={() => {
                  setSortBy(null);
                  setSortDirection(null);
                }}
              >
                No Sorting
              </Button>
            </ButtonGroup>
          </Box>

          {/* Notes List */}
          <List sx={{ maxHeight: 800, overflow: "auto" }}>
            {sortedNotes.map((note, index) => (
              <ListItem
                key={index}
                onClick={() => handleNoteClick(note)}
                secondaryAction={
                  <Typography variant="body1" color="textSecondary">
                    {note.note_date}
                  </Typography>
                }
                sx={{
                  padding: "10px",
                  borderRadius: "5px",
                  marginBottom: "10px",
                  backgroundColor: selectedNote === note ? "#f0f0f0" : "white",
                  border:
                    selectedNote === note
                      ? "1px solid #1976d2"
                      : "1px solid #ddd",
                }}
              >
                <ListItemButton>
                  <ListItemText
                    primary={note.provider_name}
                    secondary={note.note_type}
                    sx={{ color: "black" }}
                  />
                </ListItemButton>
                <ListItemText />
              </ListItem>
            ))}
          </List>
        </Box>
      </Grid>
      <Grid size={8}>
        <Box
          sx={{
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "5px",
            backgroundColor: "#fafafa",
            height: "100%",
          }}
        >
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <Avatar sx={{ bgcolor: "#1976d2", mr: 2 }}>
                {selectedNote.provider_name.charAt(0)}
              </Avatar>
              <Box>
                <Typography variant="h6" color="black">
                  {selectedNote.provider_name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {selectedNote.provider_specialty}
                </Typography>
              </Box>
            </Box>

            <Box>
              <Typography variant="body1" align="right" color="black">
                {selectedNote.note_type}
              </Typography>
              <Typography variant="body2" align="right" color="textSecondary">
                {selectedNote.note_date}
              </Typography>
            </Box>
          </Box>

          <Divider />

          <Box sx={{ mt: 2 }}>
            <Typography
              variant="body1"
              color="black"
              dangerouslySetInnerHTML={{
                __html: selectedNote.note_content,
              }}
            ></Typography>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
