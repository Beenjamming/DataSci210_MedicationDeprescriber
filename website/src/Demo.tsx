import React, { useState } from "react";
import Box from "@mui/material/Box";
import { Grid2 as Grid } from "@mui/material";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
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
        height: "calc(100vh - 48px)",
        overflowY: "auto",
        backgroundColor: value === index ? "#9ad1d4" : "inherit", // Highlight color for selected
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
  // for selected patient
  const [patientName, setPatientName] = useState<PatientName>("Donny Dunlap");

  // for menu
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMenuItemClick = (name: PatientName) => {
    setPatientName(name);
    handleClose();
  };

  // for tabs
  const [value, setValue] = useState(0);

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  // for tabs styling
  const StyledTab = styled(Tab)(({ theme }) => ({
    fontWeight: theme.typography.fontWeightBold,
    border: "1px solid", // Add a border around the tab
    borderColor: "#007a73", // Slightly darker than background
    borderBottom: "none", // Remove the underline
    borderRadius: "4px 4px 0 0", // Round the top corners for a tab-like appearance
    backgroundColor: "#e0f7fa", // Light background color
    "&.Mui-selected": {
      color: theme.palette.primary.main,
      backgroundColor: "#9ad1d4", // Slightly darker color for selected tab
      borderColor: "#007a73", // Keep the outline consistent on selection
    },
  }));

  return (
    <Grid container spacing={0.2} sx={{ height: "100vh", overflow: "hidden" }}>
      <Grid size={12}>
        <Box
          height="5vh"
          alignItems="center"
          display="flex"
          sx={{ bgcolor: "#598392" }}
        >
          <div>
            <Button
              id="demo-positioned-button"
              aria-controls={open ? "demo-positioned-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={open ? "true" : undefined}
              onClick={handleClick}
              sx={{
                bgcolor: "#598392", // Primary color for the button
                color: "white", // Text color for contrast
                fontWeight: "bold", // Increase font weight for visibility
                padding: "8px 16px", // Add padding for a larger button
                "&:hover": {
                  bgcolor: "#004d40", // Darker shade on hover
                },
              }}
            >
              Patient List
            </Button>
            <Menu
              id="demo-positioned-menu"
              aria-labelledby="demo-positioned-button"
              anchorEl={anchorEl}
              open={open}
              onClose={handleClose}
              anchorOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
            >
              <MenuItem onClick={() => handleMenuItemClick("Donny Dunlap")}>
                Donny Dunlap
              </MenuItem>
              <MenuItem onClick={() => handleMenuItemClick("Drew Buck")}>
                Drew Buck
              </MenuItem>
              <MenuItem onClick={() => handleMenuItemClick("Melinda Scott")}>
                Melinda Scott
              </MenuItem>
              <MenuItem onClick={() => handleMenuItemClick("Shelton Park")}>
                Shelton Park
              </MenuItem>
              <MenuItem onClick={() => handleMenuItemClick("Sydney Byrd")}>
                Sydney Byrd
              </MenuItem>
            </Menu>
          </div>
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
          sx={{ bgcolor: "#9ad1d4" }}
        >
          <Tabs value={value} onChange={handleChange} variant="fullWidth">
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
