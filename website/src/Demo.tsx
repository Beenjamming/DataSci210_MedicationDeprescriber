import React, { useState } from "react";
import Box from "@mui/material/Box";
import { Grid2 as Grid } from "@mui/material";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import { styled } from "@mui/material/styles";
import PatientSummary from "./Demo_summary";
import PatientNotes from "./Demo_note";
import PatientOrders from "./Demo_orders";
import PatientMedicationDischarge from "./Demo_discharge";
import PatientInfo from "./Demo_patientInfo";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
      style={{
        height: "calc(88vh - 48px)",
        overflowY: "auto",
        backgroundColor: value === index ? "#e3f2fd" : "inherit", // Very light blue for active panel
      }}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Demo() {
  type PatientName =
    | "Donny Dunlap"
    | "Drew Buck"
    | "Melinda Scott"
    | "Shelton Park"
    | "Sydney Byrd";

  const [patientName, setPatientName] = useState<PatientName>("Donny Dunlap");

  // for tabs
  const [value, setValue] = useState(0);

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handlePatientChange = (name: PatientName) => {
    setPatientName(name);
  };

  // for tabs styling
  const StyledTab = styled(Tab)(({ theme }) => ({
    fontWeight: theme.typography.fontWeightBold,
    border: "1px solid", // Add a border around the tab
    borderColor: "#004c8c", // Dark blue border
    borderBottom: "none", // Remove the underline
    backgroundColor: "#bbdefb", // Light blue background for unselected tabs
    position: "relative", // Required for pseudo-element positioning
    "&.Mui-selected": {
      color: "#ffffff", // White text for the selected tab
      backgroundColor: "#1976d2", // Primary blue for the selected tab
      borderColor: "#004c8c", // Keep the border consistent
      "&::before": {
        content: '""', // Add a pseudo-element
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: "4px", // Thickness of the underline
        backgroundColor: "#004c8c", // Dark blue underline
      },
    },
  }));

  return (
    <Grid container spacing={0.2} sx={{ height: "100vh", overflow: "hidden" }}>
      <Grid size={12}>
        <Box
          height="5vh"
          display="flex"
          alignItems="center"
          justifyContent="space-around"
          sx={{ bgcolor: "#e3f2fd" }}
        >
          {(
            [
              "Donny Dunlap",
              "Drew Buck",
              "Melinda Scott",
              "Shelton Park",
              "Sydney Byrd",
            ] as PatientName[]
          ).map((name) => (
            <Button
              key={name}
              onClick={() => handlePatientChange(name)}
              sx={{
                bgcolor: patientName === name ? "#B8DABF" : "#e3f2fd", // Slightly darker for selected
                color: "black", // Set text color to black
                fontWeight: "bold",
                "&:hover": {
                  bgcolor: "#B8DABF", // Darker green for hover
                  color: "black", // Ensure text remains black on hover
                },
              }}
            >
              {name}
            </Button>
          ))}
        </Box>
      </Grid>
      <Grid size={2}>
        <PatientInfo patient={patientName} />
      </Grid>
      <Grid size={10} sx={{ height: "100vh", overflow: "hidden" }}>
        <Box
          display="flex"
          flexDirection="column"
          height="100vh"
          width="100%"
          sx={{ bgcolor: "#f3fffe" }}
        >
          <Tabs
            value={value}
            onChange={handleChange}
            variant="fullWidth"
            TabIndicatorProps={{
              style: {
                display: "none", // Hides the default underline indicator
              },
            }}
            sx={{
              bgColor: "#e3f2fd", // Very light blue background
              borderBottom: "1px solid #004c8c", // Dark blue border below tabs
            }}
          >
            <StyledTab label="Summary" />
            <StyledTab label="Notes" />
            <StyledTab label="Orders" />
            <StyledTab label="Discharge" />
          </Tabs>
          <Divider sx={{ borderColor: "#007a73", borderBottomWidth: "2px" }} />
          <CustomTabPanel value={value} index={0}>
            <PatientSummary patient={patientName} />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={1}>
            <PatientNotes patient={patientName} />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={2}>
            <PatientOrders patient={patientName} />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={3}>
            <PatientMedicationDischarge patient={patientName} />
          </CustomTabPanel>
        </Box>
      </Grid>
    </Grid>
  );
}
