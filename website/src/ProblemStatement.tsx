import {
  Box,
  Typography,
  Grid2 as Grid,
  Card,
  CardContent,
} from "@mui/material";
import MedicationIcon from "@mui/icons-material/Medication";
import WarningIcon from "@mui/icons-material/Warning";
import InsightsIcon from "@mui/icons-material/Insights";
import PeopleIcon from "@mui/icons-material/People";

export default function ProblemStatement() {
  return (
    <Box
      id="problem-statement"
      sx={{
        backgroundColor: "#6F8F79",
        py: 5,
        px: 3,
        textAlign: "center",
        color: "white",
      }}
    >
      <Typography variant="h3" sx={{ fontWeight: "bold" }}>
        Polypharmacy: A Growing Challenge
      </Typography>
      <Typography
        variant="h5"
        sx={{ fontWeight: "bold", mb: 3, color: "#E1C16E" }}
      >
        The Use of 5+ Chronic Medication
      </Typography>

      <Grid container spacing={2} justifyContent="center">
        {/* Issue 1 */}
        <Grid size={3}>
          <Card
            sx={{
              backgroundColor: "#e9f0eb",
              height: "100%",
              textAlign: "center",
              p: 2,
              borderRadius: 2,
              boxShadow: 3,
            }}
          >
            <CardContent>
              <WarningIcon sx={{ fontSize: 50, color: "#FF6F61", mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                Rising Polypharmacy
              </Typography>
              <Typography sx={{ mt: 1 }}>
                <b>
                  <span style={{ color: "red" }}>37%</span>
                </b>{" "}
                of adults and a growing number of older adults (65+) experience
                polypharmacy, where rates have{" "}
                <b>
                  <span style={{ color: "red" }}>tripled</span>
                </b>{" "}
                (12.8% to 39.0%).
              </Typography>
              <Typography
                variant="caption"
                sx={{ mt: 2, display: "block", color: "#003249" }}
              >
                Source:{" "}
                <a
                  href="https://pmc.ncbi.nlm.nih.gov/articles/PMC10337167/#:~:text=A%20recent%20meta%2Danalysis%20reported,in%20different%20populations%20%5B4%5D"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    color: "#12737D",
                    textDecoration: "none",
                    fontWeight: "bold",
                  }}
                >
                  Meta-analysis on Polypharmacy Prevalence
                </a>
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Issue 2 */}
        <Grid size={3}>
          <Card
            sx={{
              backgroundColor: "#e9f0eb",
              height: "100%",
              textAlign: "center",
              p: 2,
              borderRadius: 2,
              boxShadow: 3,
            }}
          >
            <CardContent>
              <MedicationIcon sx={{ fontSize: 50, color: "#6CC24A", mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                Unnecessary Medications Continued
              </Typography>
              <Typography sx={{ mt: 1 }}>
                Many medications started during inpatient stays fail to be
                discontinued at discharge, leading to long-term use without a
                diagnosis.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Issue 3 */}
        <Grid size={3}>
          <Card
            sx={{
              backgroundColor: "#e9f0eb",
              height: "100%",
              textAlign: "center",
              p: 2,
              borderRadius: 2,
              boxShadow: 3,
            }}
          >
            <CardContent>
              <InsightsIcon sx={{ fontSize: 50, color: "#007BFF", mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                Lack of Time
              </Typography>
              <Typography sx={{ mt: 1 }}>
                Providers face significant time constraints when evaluating
                medication needs at discharge, exacerbated by a shortage of
                healthcare staff.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Issue 4 */}
        <Grid size={3}>
          <Card
            sx={{
              backgroundColor: "#e9f0eb",
              height: "100%",
              textAlign: "center",
              p: 2,
              borderRadius: 2,
              boxShadow: 3,
            }}
          >
            <CardContent>
              <PeopleIcon sx={{ fontSize: 50, color: "#FFB400", mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                Adverse Outcomes
              </Typography>
              <Typography sx={{ mt: 1 }}>
                Polypharmacy is linked to adverse drug events, reduced patient
                safety, and diminished quality of life.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
