import React from "react";
import { patientData, PatientName } from "./patientData";
import { Divider, Grid2 as Grid, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import Avatar from "@mui/material/Avatar";

interface PatientNotesProps {
  patient: PatientName;
}

export default function PatientNotes(props: PatientNotesProps) {
  const { notes } = patientData[props.patient];

  const [selectedNote, setSelectedNote] = React.useState(notes[0]);

  // Function to handle click event for a note
  const handleNoteClick = (note: (typeof notes)[0]) => {
    setSelectedNote(note);
  };

  return (
    <Grid container spacing={2}>
      <Grid size={4}>
        <Box>
          <List sx={{ maxHeight: 600, overflow: "auto", bgcolor: "white" }}>
            {notes.map((note, index) => (
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
            <Typography variant="body1" color="black">
              {selectedNote.note_content}
            </Typography>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
