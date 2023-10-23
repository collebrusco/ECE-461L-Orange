import React from "react";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Navbar from "../components/Navbar";

function Layout(props) {
  const { title, buttons, children } = props;

  React.useEffect(() => {
    if (title) {
      document.title = title;
    }
  });

  return (
    <Box sx={{ display: "flex" }}>
      <Navbar title={title}>{buttons}</Navbar>
      <Box
        component="main"
        sx={{
          backgroundColor: "#f5f5f5",
          flexGrow: 1,
          height: "100vh",
          overflow: "auto",
        }}
      >
        {/* Placeholder */}
        <Toolbar />

        {/* Main Content */}
        {children}
      </Box>
    </Box>
  );
}

export default Layout;
