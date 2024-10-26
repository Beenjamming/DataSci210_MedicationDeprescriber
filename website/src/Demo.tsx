import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { Grid2 as Grid } from "@mui/material";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";
import PatientSummary from "./Demo_summary";
import PatientNotes from "./Demo_note";
import PatientOrders from "./Demo_orders";
import PatientMedicationDischarge from "./Demo_discharge";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Demo() {
  // for menu
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  // for tabs
  const [value, setValue] = React.useState(0);

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  // for tabs styling
  const StyledTab = styled(Tab)(({ theme }) => ({
    fontWeight: theme.typography.fontWeightBold,
  }));

  return (
    <Grid container spacing={0.2} sx={{ height: "100vh", overflow: "hidden" }}>
      <Grid size={12}>
        <Box
          height="2.5vh"
          alignItems="center"
          display="flex"
          sx={{ bgcolor: "white" }}
        >
          <div>
            <Button
              id="demo-positioned-button"
              aria-controls={open ? "demo-positioned-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={open ? "true" : undefined}
              onClick={handleClick}
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
              <MenuItem onClick={handleClose}>Donald Duck</MenuItem>
              <MenuItem onClick={handleClose}>Snoopy</MenuItem>
              <MenuItem onClick={handleClose}>Perry the Platypus</MenuItem>
            </Menu>
          </div>
        </Box>
      </Grid>
      <Grid size={2}>
        <Box height="100vh" sx={{ bgcolor: "#9ad1d4", pt: 1 }}>
          <Box display="flex" flexDirection="column" alignItems="center">
            <Avatar sx={{ bgcolor: "primary.main", width: 100, height: 100 }}>
              DD
            </Avatar>
            <Typography variant="h6" color="black">
              <b>Donald Duck</b>
            </Typography>
            <Typography color="black">
              <b>Age:</b> 51
              <br />
              <b>Sex:</b> Male
              <br />
              <b>Race:</b> Duck
            </Typography>
          </Box>
          <Divider
            flexItem
            sx={{ borderColor: "black", borderBottomWidth: 2, mt: 1 }}
          />
          <Box sx={{ m: 1 }}>
            <Typography color="#8c1f7a">
              <b>Precautions</b>
            </Typography>
            <Typography color="black">Fall precautions</Typography>
          </Box>
        </Box>
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
          <CustomTabPanel value={value} index={0}>
            <PatientSummary patient="Donald" />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={1}>
            <PatientNotes patient="Donald" />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={2}>
            <PatientOrders patient="Donald" />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={3}>
            <PatientMedicationDischarge patient="Donald" />
          </CustomTabPanel>
        </Box>
      </Grid>
    </Grid>
  );
}
