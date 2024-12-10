import * as React from "react";
import { Typography, Box } from "@mui/material";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";
import { TypeAnimation } from "react-type-animation";
import backgroundImage from "./assets/landingPage_blur.jpg";
// import MedicationIcon from "@mui/icons-material/Medication";
// import SpeedIcon from "@mui/icons-material/Speed";
// import SavingsIcon from "@mui/icons-material/Savings";
import "./LandingPageContainer.css";
import About_Us from "./About_Us.tsx";
// import ImpactCard from "./Impact.tsx";
import MethodologyTabs from "./Methodology.tsx";
import ProblemStatement from "./ProblemStatement.tsx";
import WhyRxReduce from "./Why_RxReduce.tsx";
import demoVideo from "./assets/RxReduce_Demo.mp4";

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
          sx={{
            padding: "4px 16px", // Larger padding for a bigger button
            fontSize: "1.3rem", // Larger font size for text
            borderRadius: "8px", // Adjust border radius for a rounded look
            minWidth: "150px", // Ensure a minimum width
          }}
        >
          Live Demo
        </Button>
        <Typography variant="h5" color="gray" sx={{ mt: 2 }}>
          Watch the video below for a demo of our product.
        </Typography>
        <Box
          mt={4}
          width="80%"
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <video width="60%" controls>
            <source src={demoVideo} type="video/mp4" />
          </video>
        </Box>
      </Box>
      <Box
        id="problem-statement"
        sx={{
          backgroundColor: "#6F8F79",
          textAlign: "center",
          color: "#003249",
        }}
      >
        <ProblemStatement />
      </Box>
      <Box
        id="why-rxreduce"
        sx={{
          backgroundColor: "#6F8F79",
          textAlign: "center",
          color: "#003249",
        }}
      >
        <WhyRxReduce />
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

      {/* <Box
        id="impact"
        sx={{
          backgroundColor: "#1c1f33",
          color: "#ffffff",
          py: 5,
          textAlign: "center",
        }}
      >
        <Typography variant="h3" gutterBottom sx={{ fontWeight: "bold" }}>
          Our Solution's Impact
        </Typography>
        <Grid container justifyContent="center" spacing={3}>
          <ImpactCard
            title="Simplify Medication Regimens"
            icon={<MedicationIcon sx={{ fontSize: 50 }} />}
            blurb="Enhance patient outcomes by simplifying medication routines at discharge."
            details="Our tool identifies and recommends discontinuation of unnecessary medications at discharge, 
            helping to reduce polypharmacy. Leveraging patient data, we pinpoint key symptoms and conditions to feed into
            evidence-based deprescribing algorithms, enabling precise recommendations for medication 
            discontinuation at the time of discharge."
          />
          <ImpactCard
            title="Increase Discharge Efficiency"
            icon={<SpeedIcon sx={{ fontSize: 50 }} />}
            blurb="Streamline medication at discharge for providers, saving valuable time."
            details="Our tool assists providers by highlighting key notes and patient information,
            making it easy to reference essential patient details alongside our recommendations. 
            This approach supports providers in making informed decisions about 
            medication management at discharge, ensuring unnecessary medications are identified and discontinued."
          />
          <ImpactCard
            title="Reduce Healthcare Costs"
            icon={<SavingsIcon sx={{ fontSize: 50 }} />}
            blurb="Lower healthcare costs with optimized medication use."
            details="Eliminating unnecessary medications through deprescribing helps lower costs for both patients and the broader healthcare system."
          />
        </Grid>
      </Box> */}

      <Box
        id="methodology"
        minHeight="80vh" // Controlled height for spacing
        display="flex"
        flexDirection="column"
        alignItems="center"
        sx={{
          bgcolor: "#e0e4e4",
        }}
      >
        {/* <Typography
          variant="h3"
          align="center"
          sx={{ mb: 2, fontWeight: "bold", color: "#1c1f33" }}
        >
          Methodology
        </Typography> */}

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
