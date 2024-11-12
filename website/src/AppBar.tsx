import { Toolbar } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";
import Logo from "./assets/logo.svg";

export default function ButtonAppBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ backgroundColor: "#12737D", padding: 0 }}>
        <Toolbar sx={{ minHeight: 64, padding: 0 }}>
          <Button
            component={RouterLink}
            to="/DataSci210_MedicationDeprescriber/"
            color="inherit"
            sx={{
              textTransform: "none",
              fontWeight: 700,
              display: "flex",
              alignItems: "center",
              color: "white",
              "&:hover": {
                color: "#C6E2F0",
              },
              "&:active": {
                color: "#C6E2F0",
              },
            }}
          >
            <Box
              component="img"
              src={Logo}
              alt="Logo"
              sx={{
                width: 50, // Adjust width to fit
                height: 50, // Adjust height to fit
                mr: 1, // Adjust margin-right for spacing
              }}
            />
            <Typography variant="h3"> RxReduce </Typography>
          </Button>
          <Box sx={{ ml: 4, display: "flex" }}>
            <Button
              sx={{
                color: "inherit",
                "&:hover": {
                  color: "#C6E2F0",
                },
                "&:active": {
                  color: "#C6E2F0",
                },
              }}
              href="#our-mission"
            >
              <Typography>Our Mission</Typography>
            </Button>
            <Button
              sx={{
                color: "inherit",
                "&:hover": {
                  color: "#C6E2F0",
                },
                "&:active": {
                  color: "#C6E2F0",
                },
              }}
              href="#impact"
            >
              <Typography>Impact</Typography>
            </Button>
            {/* <Button
              component={RouterLink}
              to="/DataSci210_MedicationDeprescriber/Demo"
              sx={{
                color: "inherit",
                "&:hover": {
                  color: "#C6E2F0",
                },
                "&:active": {
                  color: "#C6E2F0",
                },
              }}
            >
              <Typography>Live Demo</Typography>
            </Button> */}
            <Button
              sx={{
                color: "inherit",
                "&:hover": {
                  color: "#C6E2F0",
                },
                "&:active": {
                  color: "#C6E2F0",
                },
              }}
              href="#methodology"
            >
              <Typography>Methodology</Typography>
            </Button>
            <Button
              sx={{
                color: "inherit",
                "&:hover": {
                  color: "#C6E2F0",
                },
                "&:active": {
                  color: "#C6E2F0",
                },
              }}
              href="#our-team"
            >
              <Typography>Our Team</Typography>
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
