import { useState, ReactNode } from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import "./Impact.css";

interface FlipCardProps {
  title: string;
  icon: ReactNode; // The path to the image
  blurb: string;
  details: string;
}

export default function ImpactCard({
  title,
  icon,
  blurb,
  details,
}: FlipCardProps) {
  const [flipped, setFlipped] = useState(false);

  return (
    <Card
      className={`flip-card ${flipped ? "flipped" : ""}`}
      onClick={() => setFlipped(!flipped)}
      sx={{
        width: 300,
        height: 400,
        margin: "1rem",
      }}
    >
      <Box className="flip-card-inner">
        {/* Front Side */}
        <CardContent
          className="flip-card-front"
          sx={{
            backgroundColor: "#f3fefe", // Set desired front color here
            color: "#000000", // Optional: adjust text color
          }}
        >
          {icon}
          <Typography variant="h5" sx={{ mt: 2, fontWeight: "bold" }}>
            {title}
          </Typography>
          <Typography variant="body1" sx={{ mt: 2 }}>
            {blurb}
          </Typography>
          <Typography
            variant="caption"
            sx={{ mt: 2, fontStyle: "italic", color: "black" }}
          >
            Click to flip and see more
          </Typography>
        </CardContent>

        {/* Back Side */}
        <CardContent className="flip-card-back">
          <Typography variant="body1">{details}</Typography>
        </CardContent>
      </Box>
    </Card>
  );
}
