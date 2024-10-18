import { Toolbar } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";

export default function ButtonAppBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            RxReduce
          </Typography>
          <Button
            component={RouterLink}
            to="/DataSci210_MedicationDeprescriber/Demo"
            color="inherit"
          >
            Demo
          </Button>
          <Button color="inherit"> About </Button>
          <Button color="inherit"> Process </Button>
          <Button color="inherit"> Documentation </Button>
          <Button color="inherit"> About </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
