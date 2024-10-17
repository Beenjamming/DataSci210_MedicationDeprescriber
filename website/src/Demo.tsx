import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { Grid2 as Grid } from "@mui/material";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";

export default function Demo() {
  return (
    <Grid container spacing={0.2}>
      <Grid size={12}>
        <Box height="3vh" />
      </Grid>
      <Grid size={2}>
        <Box
          display="flex"
          justifyContent="center"
          flexDirection="column"
          alignItems="center"
          height="100vh"
          sx={{ bgcolor: "#9ad1d4" }}
        >
          <Box>
            <Avatar sx={{ bgcolor: "primary.main", width: 100, height: 100 }}>
              DD
            </Avatar>
            <Typography variant="h6">Donald Duck</Typography>
          </Box>
          <Divider flexItem sx={{ borderColor: "gray" }} />
          {/* <Box>
            <Typography variant="h6" sx={{ color: "red" }}>
              Allergies
            </Typography>
            <Typography variant="h6">More Info?</Typography>
          </Box> */}
        </Box>
      </Grid>
      <Grid size={10}>
        <Box
          display="flex"
          flexDirection="column"
          height="100vh"
          width="100%"
          sx={{ bgcolor: "#9ad1d4" }}
        >
          <Tabs variant="fullWidth">
            <Tab label="Summary" />
            <Tab label="Notes" />
            <Tab label="Orders" />
            <Tab label="Discharge" />
          </Tabs>
        </Box>
      </Grid>
    </Grid>
  );
}
