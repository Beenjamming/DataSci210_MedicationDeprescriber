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
  palette: { primary: { main: "#1f7a8c" } },
  typography: {
    fontFamily: "Gill Sans",
  },
});
const BASE_PATH = "/DataSci210_MedicationDeprescriber/";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path={BASE_PATH} element={<App />}>
      <Route path={BASE_PATH} element={<LandingPageContainer />} />
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
