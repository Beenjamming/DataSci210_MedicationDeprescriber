import { Box, Typography, Grid2 as Grid } from "@mui/material";
import SettingsSuggestIcon from "@mui/icons-material/SettingsSuggest";
import HealthAndSafetyIcon from "@mui/icons-material/HealthAndSafety";
import ContentPasteSearchIcon from "@mui/icons-material/ContentPasteSearch";
import SpeedIcon from "@mui/icons-material/Speed";
import MedicationIcon from "@mui/icons-material/Medication";

export default function WhyRxReduce() {
  return (
    <Box
      sx={{
        backgroundColor: "#f3fffe",
        textAlign: "center",
        color: "#003249",
        py: 5,
        px: 3,
      }}
    >
      <Typography variant="h3" sx={{ fontWeight: "bold", mb: 3 }}>
        Why Choose RxReduce?
      </Typography>

      <Grid container spacing={4} justifyContent="center">
        {/* Card 1: Streamline Decision-Making */}
        <Grid size={4}>
          <Box
            sx={{
              backgroundColor: "#12897D",
              color: "#ffffff",
              p: 3,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              height: "250px",
            }}
          >
            <SettingsSuggestIcon sx={{ fontSize: 60, mr: 2 }} />
            <Box textAlign="left">
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
                Streamline Decision-Making
              </Typography>
              <Typography>
                Using advanced{" "}
                <strong>Retrieval-Augmented Generation (RAG)</strong>{" "}
                technology, RxReduce quickly analyzes patient data, clinical
                notes, and diagnoses to pinpoint medications that may no longer
                be necessary—saving time and improving care accuracy.
              </Typography>
            </Box>
          </Box>
        </Grid>

        {/* Card 2: Enhance Medication Safety */}
        <Grid size={4}>
          <Box
            sx={{
              backgroundColor: "#2A9D8F",
              color: "#ffffff",
              p: 3,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              height: "250px",
            }}
          >
            <HealthAndSafetyIcon sx={{ fontSize: 60, mr: 2 }} />
            <Box textAlign="left">
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
                Enhance Medication Safety
              </Typography>
              <Typography>
                RxReduce flags potential medication redundancies, ensuring that
                patients only continue with treatments that truly benefit them,
                while also simplifying their medication regimen.
              </Typography>
            </Box>
          </Box>
        </Grid>

        {/* Card 3: Evidence-Based Recommendations */}
        <Grid size={4}>
          <Box
            sx={{
              backgroundColor: "#E76F51",
              color: "#ffffff",
              p: 3,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              height: "250px",
            }}
          >
            <ContentPasteSearchIcon sx={{ fontSize: 60, mr: 2 }} />
            <Box textAlign="left">
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
                Evidence-Based Recommendations
              </Typography>
              <Typography>
                RxReduce delivers actionable insights based on the latest
                guidelines, like the Proton Pump Inhibitor (PPI) deprescribing
                algorithm, ensuring every recommendation is rooted in clinical
                evidence.
              </Typography>
            </Box>
          </Box>
        </Grid>

        {/* Card 4: Improved Care Efficiency */}
        <Grid size={6}>
          <Box
            sx={{
              backgroundColor: "#F4A261",
              color: "#ffffff",
              p: 3,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              height: "150px",
            }}
          >
            <SpeedIcon sx={{ fontSize: 60, mr: 2 }} />
            <Box textAlign="left">
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
                Improved Care and Discharge Efficiency
              </Typography>
              <Typography>
                RxReduce processes vast amounts of clinical data swiftly,
                helping providers make critical decisions without being bogged
                down by information overload.
              </Typography>
            </Box>
          </Box>
        </Grid>

        {/* Card 5: Reduce Medication Burden and Cost*/}
        <Grid size={6}>
          <Box
            sx={{
              backgroundColor: "#264653",
              color: "#ffffff",
              p: 3,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              height: "150px",
            }}
          >
            <MedicationIcon sx={{ fontSize: 60, mr: 2 }} />
            <Box textAlign="left">
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 1 }}>
                Reduce Medication Burden and Cost
              </Typography>
              <Typography>
                By identifying and removing unnecessary medications, RxReduce
                helps minimize the burden of polypharmacy, improving patient
                outcomes and quality of life. Consequentially, reducing the cost
                of healthcare.
              </Typography>
            </Box>
          </Box>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Transform your discharge process with RxReduce – reducing
          polypharmacy, one medication at a time.
        </Typography>
      </Box>
    </Box>
  );
}
