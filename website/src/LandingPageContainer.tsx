import * as React from "react";
import { Typography, Box, Grid2 as Grid } from "@mui/material";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";
import { TypeAnimation } from "react-type-animation";
import backgroundImage from "./assets/landingPage_blur.jpg";
import MedicationIcon from "@mui/icons-material/Medication";
import SpeedIcon from "@mui/icons-material/Speed";
import SavingsIcon from "@mui/icons-material/Savings";
import "./LandingPageContainer.css";
import About_Us from "./About_Us.tsx";
import ImpactCard from "./Impact.tsx";
import MethodologyTabs from "./Methodology.tsx";

const CURSOR_CLASS_NAME = "custom-type-animation-cursor";

export default function LandingPageContainer() {
  return (
    <React.Fragment>
      <Box
        display="flex"
        justifyContent="center"
        flexDirection="column"
        alignItems="center"
        minHeight="100vh"
        sx={{
          backgroundImage: `url(${backgroundImage})`,
          backgroundSize: "cover", // Ensures the image covers the entire Box
          backgroundPosition: "center", // Centers the image
          backgroundRepeat: "no-repeat",
          overflow: "auto",
        }}
      >
        <TypeAnimation
          cursor={false}
          className={CURSOR_CLASS_NAME}
          sequence={[
            "Welcome to RxReduce!",
            0,
            (el) => el?.classList.remove(CURSOR_CLASS_NAME),
          ]}
          wrapper="span"
          speed={50}
          style={{
            fontSize: "5em",
            color: "#003249",
            fontWeight: "bold",
            display: "block",
            textAlign: "center",
          }}
          repeat={1}
        />

        <Typography variant="h4" color="#003249" align="center" gutterBottom>
          A discharge medication deprescribing agent.
        </Typography>

        <Button
          component={RouterLink}
          to="/DataSci210_MedicationDeprescriber/Demo"
          variant="contained"
          color="primary"
        >
          Live Demo
        </Button>
        <Box
          mt={4}
          width="80%"
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <video width="60%" controls>
            {/* <source src={demoVideo} type="video/mp4" /> */}
            Your browser does not support the video tag.
          </video>
        </Box>
      </Box>
      <Box
        id="our-mission"
        height="50vh"
        display="flex"
        justifyContent="center"
        alignItems="center"
        sx={{
          backgroundColor: "#12897D",
          textAlign: "center",
          color: "#f3fffe",
          py: 2,
          px: 5,
        }}
      >
        <Typography
          variant="h2"
          align="center"
          sx={{ fontWeight: "bold", mb: 2 }}
        >
          Our Mission
        </Typography>

        <Box
          sx={{
            width: "4px",
            height: "100px",
            backgroundColor: "#f3fffe",
            mx: 8,
            transform: "rotate(20deg)", // Adjust rotation as needed
          }}
        />

        <Typography variant="h3" component="h1">
          We want to make healthcare as{" "}
          <span style={{ color: "#BFFF00" }}>efficient</span> and{" "}
          <span style={{ color: "#BFFF00" }}>safe</span> as possible through
          advanced data science techniques.
        </Typography>
      </Box>

      <Box
        sx={{
          backgroundColor: "#1c1f33",
          color: "#ffffff",
          py: 5,
          textAlign: "center",
        }}
      >
        <Typography variant="h3" gutterBottom>
          Our Impact
        </Typography>
        <Grid container justifyContent="center" spacing={3}>
          <ImpactCard
            title="Simplify Medication Regimens"
            icon={<MedicationIcon sx={{ fontSize: 50 }} />}
            blurb="Enhance patient outcomes by simplifying medication routines."
            details="Our tool helps identify and discontinue unnecessary medications at discharge, aimed to decrease polypharmacy."
          />
          <ImpactCard
            title="Increase Discharge Efficiency"
            icon={<SpeedIcon sx={{ fontSize: 50 }} />}
            blurb="Streamline discharge for providers, saving valuable time."
            details="Our tool helps providers identify key notes that assists them during discharge to identify unncessary medications and evidence-based notes that support the recommendation."
          />
          <ImpactCard
            title="Reduce Healthcare Costs"
            icon={<SavingsIcon sx={{ fontSize: 50 }} />}
            blurb="Lower healthcare costs with optimized medication use."
            details="Deprescribing unnecessary medications reduces medication costs for patients and the healthcare system as a whole."
          />
        </Grid>
      </Box>

      <Box
        id="methodology"
        minHeight="80vh" // Controlled height for spacing
        display="flex"
        flexDirection="column"
        alignItems="center"
        sx={{
          bgcolor: "#e0e4e4",
          py: 3,
        }}
      >
        {/* Methodology Title */}
        <Typography
          variant="h3"
          align="center"
          sx={{ mb: 2, fontWeight: "bold", color: "#1c1f33" }}
        >
          Methodology
        </Typography>

        {/* Tabs for Methodology */}
        <MethodologyTabs />
      </Box>

      {/* Documentation Section */}
      <Box
        id="our-team"
        sx={{
          backgroundColor: "#1c1f33",
          color: "#ffffff",
          py: 5,
          px: 3,
          textAlign: "center",
        }}
      >
        <About_Us />{" "}
      </Box>
    </React.Fragment>
  );
}
