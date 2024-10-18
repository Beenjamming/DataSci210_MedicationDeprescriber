import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";

export default function LandingPageContainer() {
  return (
    <React.Fragment>
      <Box
        display="flex"
        justifyContent="center"
        flexDirection="column"
        alignItems="center"
        height="100vh"
        sx={{ bgcolor: "#9ad1d4" }}
      >
        <Typography variant="h3" color="#003249" align="center" gutterBottom>
          Welcome to RxReduce!
        </Typography>
        <Typography variant="h4" color="#003249" align="center" gutterBottom>
          A discharge medication deprescribing agent.
        </Typography>
        <Button
          component={RouterLink}
          to="/DataSci210_MedicationDeprescriber/Demo"
          variant="contained"
          color="primary"
        >
          Demo
        </Button>
      </Box>
    </React.Fragment>
  );
}
