import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import Demo from "./Demo.tsx";
import "./index.css";
import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import { Route } from "react-router-dom";
import LandingPageContainer from "./LandingPageContainer.tsx";

const theme = createTheme({
  palette: {
    primary: {
      main: "#12737D", // Teal Blue
    },
    secondary: {
      main: "#29C3CC", // Bright Aqua
    },
    background: {
      default: "#D6F0E0", // Light Seafoam for background
      paper: "#6F8F79", // Muted Forest Green for boxes
    },
    text: {
      primary: "#2E3D46", // Deep Blue Gray for text
    },
  },
  typography: {
    fontFamily: "Gill Sans",
  },
});
const BASE_PATH = "/DataSci210_MedicationDeprescriber/";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path={BASE_PATH} element={<App />}>
      <Route index element={<LandingPageContainer />} />
      {/* <Route path={BASE_PATH} element={<LandingPageContainer />} /> */}
      <Route path={`${BASE_PATH}Demo`} element={<Demo />} />
    </Route>,
  ),
);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <CssBaseline />
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </StrictMode>,
);
