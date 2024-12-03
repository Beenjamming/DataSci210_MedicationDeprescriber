import React, { useState } from "react";
import {
  Box,
  Grid2 as Grid,
  Tab,
  Tabs,
  Divider,
  Select,
  MenuItem,
  Typography,
  SelectChangeEvent,
} from "@mui/material";
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
        backgroundColor: value === index ? "#e3f2fd" : "inherit",
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
    | "Sydney Byrd"
    | "Willow Harper";

  const [patientName, setPatientName] = useState<PatientName>("Donny Dunlap");
  const [value, setValue] = useState(0);

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handlePatientChange = (event: SelectChangeEvent<PatientName>) => {
    setPatientName(event.target.value as PatientName);
  };

  const StyledTab = styled(Tab)(({ theme }) => ({
    fontWeight: theme.typography.fontWeightBold,
    border: "1px solid",
    borderColor: "#004c8c",
    borderBottom: "none",
    backgroundColor: "#bbdefb",
    position: "relative",
    "&.Mui-selected": {
      color: "#ffffff",
      backgroundColor: "#1976d2",
      borderColor: "#004c8c",
      "&::before": {
        content: '""',
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: "4px",
        backgroundColor: "#004c8c",
      },
    },
  }));

  return (
    <Grid container spacing={0.2} sx={{ height: "100vh", overflow: "hidden" }}>
      {/* Header Section */}
      <Grid size={12}>
        <Box
          height="9vh"
          display="flex"
          alignItems="center"
          px={4}
          sx={{ bgcolor: "#e3f2fd" }}
        >
          {/* "Select Patient:" Label */}
          <Typography
            variant="h6"
            fontWeight="bold"
            color="#004c8c"
            sx={{ mr: 2 }}
          >
            Select Patient:
          </Typography>

          {/* Patient Selector */}
          <Select
            value={patientName}
            onChange={handlePatientChange}
            displayEmpty
            sx={{
              minWidth: 200,
              bgcolor: "white",
              borderRadius: 1,
              "& .MuiSelect-select": { fontWeight: "bold" },
            }}
          >
            {(
              [
                "Donny Dunlap",
                "Drew Buck",
                "Melinda Scott",
                "Shelton Park",
                "Sydney Byrd",
                "Willow Harper",
              ] as PatientName[]
            ).map((name) => (
              <MenuItem
                key={name}
                value={name}
                sx={{
                  bgcolor: "white", // White background for menu items
                  "&:hover": {
                    bgcolor: "#f5f5f5", // Light gray on hover
                  },
                }}
              >
                {name}
              </MenuItem>
            ))}
          </Select>
        </Box>
      </Grid>

      {/* Patient Info */}
      <Grid size={2}>
        <PatientInfo patient={patientName} />
      </Grid>

      {/* Tabs Section */}
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
                display: "none",
              },
            }}
            sx={{
              bgColor: "#e3f2fd",
              borderBottom: "1px solid #004c8c",
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
