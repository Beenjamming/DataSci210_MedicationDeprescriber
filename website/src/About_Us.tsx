import { Typography, Box, Grid2 as Grid, Avatar } from "@mui/material";
import BenImage from "./assets/team_images/ben.jpeg";
import ReedImage from "./assets/team_images/reed.jpeg";
import GrayImage from "./assets/team_images/gray.jpg";
import KrisImage from "./assets/team_images/kris.jpg";
import JoannaImage from "./assets/team_images/joanna.jpeg";

export default function AboutUs() {
  const teamMembers = [
    { name: "Ben Michaels", image: BenImage },
    { name: "Reed Evans", image: ReedImage },
    { name: "Gray Selby", image: GrayImage },
    { name: "Kris Riedman", image: KrisImage },
    { name: "Joanna Yang", image: JoannaImage },
  ];
  return (
    <Box>
      {/* <Box sx={{ backgroundColor: "#EFF6E0", color: "#000000", py: 5, px: 3 }}>
        <Grid container direction="row" alignItems="center" spacing={4}>
          <Grid size={4}>
            <Typography variant="h3" component="h1" gutterBottom>
              About The Team
            </Typography>
          </Grid>
          <Grid size={8}>
            <Typography variant="body1" sx={{ color: "#000000" }}>
              Our team plans to address the challenge of ensuring medications
              are safely discontinued at discharge. Due to the high volume of
              notes and limited time available, providers sometimes miss
              discontinuing medications. Our innovative RAG-based system
              integrates with a PPI deprescribing algorithm, assisting providers
              in identifying relevant recommendations quickly and accurately,
              enhancing patient safety.
            </Typography>
          </Grid>
        </Grid>
      </Box> */}
      <Box
        sx={{
          backgroundColor: "#1c1f33",
          color: "#ffffff",
          py: 5,
          px: 3,
          textAlign: "center",
        }}
      >
        <Typography variant="h4" component="h2" gutterBottom>
          Meet The Team
        </Typography>
        <Grid container spacing={2} justifyContent="center">
          {teamMembers.map((member, index) => (
            <Grid size={2} key={index}>
              <Avatar
                alt={member.name}
                src={member.image}
                sx={{
                  width: 120,
                  height: 120,
                  margin: "auto",
                  objectFit: "cover",
                  borderRadius: 0,
                }}
              />
              <Typography variant="body1" sx={{ mt: 1 }}>
                {member.name}
              </Typography>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Box>
  );
}
