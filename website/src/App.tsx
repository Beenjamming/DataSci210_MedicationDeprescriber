import React from "react";
import AppBar from "./AppBar";
import { Outlet } from "react-router-dom";
import "./App.css";

export default function App() {
  return (
    <React.Fragment>
      <AppBar />
      <Outlet />
    </React.Fragment>
  );
}
