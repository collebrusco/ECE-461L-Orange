import React from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { SnackbarProvider } from "notistack";
import SnackbarCloseButton from "./components/SnackbarCloseButton";
import AuthProvider from "./components/AuthProvider";
import Router from "./Router";

const theme = createTheme({
  typography: {
    fontFamily: "'IBM Plex Sans', 'sans-serif'",
    button: {
      textTransform: "none",
    },
  },
  palette: {
    neutral: {
      main: "#f3f3f3",
      dark: "#ccc",
      contrastText: "#2d2e30",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider
        action={(key) => <SnackbarCloseButton key={key} />}
        dense
        preventDuplicate
      />
      <AuthProvider>
        <Router />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
