import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";
import StorageIcon from "@mui/icons-material/Storage";
import { AccountTree, PrecisionManufacturing } from "@mui/icons-material";
import { Typography } from "@mui/material";
import DeprescribingPicture from "./assets/deprescribing_algorithm.png";
import toolAlgorithm from "./assets/tool_algorithm.png";
import SettingsIcon from "@mui/icons-material/Settings";

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
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3, color: "#1c1f33" }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export default function BasicTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
          variant="fullWidth"
        >
          <Tab
            icon={<StorageIcon />}
            iconPosition="start"
            label="Our Data"
            {...a11yProps(0)}
            sx={{
              fontSize: "1.2rem",
              color: value === 0 ? "white" : "#1c1f33", // Black when not active, white when active
              bgcolor: value === 0 ? "#12897D" : "transparent",
              "&.Mui-selected": {
                outline: `2px solid #12897D`,
                color: "white",
              },
            }}
          />
          <Tab
            icon={<AccountTree />}
            iconPosition="start"
            label="Deprescribing Algorithm"
            {...a11yProps(1)}
            sx={{
              fontSize: "1.2rem",
              color: value === 1 ? "white" : "#1c1f33", // Black when not active, white when active
              bgcolor: value === 1 ? "#12897D" : "transparent",
              "&.Mui-selected": {
                outline: `2px solid #12897D`,
                color: "white",
              },
            }}
          />
          <Tab
            icon={<PrecisionManufacturing />}
            iconPosition="start"
            label="Our Tool"
            {...a11yProps(2)}
            sx={{
              fontSize: "1.2rem",
              color: value === 2 ? "white" : "#1c1f33", // Black when not active, white when active
              bgcolor: value === 2 ? "#12897D" : "transparent",
              "&.Mui-selected": {
                outline: `2px solid #12897D`,
                color: "white",
              },
            }}
          />
          <Tab
            icon={<SettingsIcon />}
            iconPosition="start"
            label="Integration"
            {...a11yProps(3)}
            sx={{
              fontSize: "1.2rem",
              color: value === 3 ? "white" : "#1c1f33", // Black when not active, white when active
              bgcolor: value === 3 ? "#12897D" : "transparent",
              "&.Mui-selected": {
                outline: `2px solid #12897D`,
                color: "white",
              },
            }}
          />
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={0}>
        <Typography variant="h5">Data</Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          We are using de-identified UCSF Health Deidentified Information
          Commons Data for the development and testing of the project. It is
          pulled using a query into the MS SQL Server.
        </Typography>
        <Typography variant="h5">Sampled Patient Information</Typography>
        <Typography variant="body1">
          Our patient criterion includes any individual 18 years or older and
          came in on, were administered, or discharged on a proton pump
          inhibitor (PPI) relative to their inpatient stay. We identified 520
          unique patients with 522 unique encounters. Our patient population
          spans 18 to 90 years of age. All patients were discharged in September
          2023 with admission dates spanning May 2023 to September 2023.
        </Typography>
      </CustomTabPanel>
      <CustomTabPanel value={value} index={1}>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <Box sx={{ flex: 1, pr: 2 }}>
            <p>
              Our focus lies on Proton Pump Inhibitors (PPI) and identifying
              recommendation of continuing, deprescribing, or stopping
              medication prescription at discharge. Our goal is to identify the
              symptoms and conditions listed within the algorithm from advanced
              data science techniques and supply it to this deprescription
              algorithm to recommend an option to the provider.
            </p>
          </Box>
          <Box sx={{ flexShrink: 0 }}>
            <img
              src={DeprescribingPicture}
              alt="Description"
              style={{ width: "800px", height: "auto" }}
            />
          </Box>
        </Box>
      </CustomTabPanel>
      <CustomTabPanel value={value} index={2}>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img
            src={toolAlgorithm}
            alt="Description"
            style={{ width: "800px", height: "auto" }}
          />
        </Box>
      </CustomTabPanel>
      <CustomTabPanel value={value} index={3}>
        API in EPIC
      </CustomTabPanel>
    </Box>
  );
}
