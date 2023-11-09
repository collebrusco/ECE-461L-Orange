import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import SignInOutButton from "./SignInOutButton";
import { useAuth, AUTH_STATUS } from "./AuthProvider";

function Navbar(props) {
  const { user: { username }, status } = useAuth();
  const hasSignIn = status === AUTH_STATUS.AUTHENTICATED;
  const { title, children } = props;

  return (
    <AppBar component="nav" position="absolute">
      <Toolbar>
        <Typography
          component="h1"
          variant="h6"
          color="inherit"
          noWrap
          sx={{ flexGrow: 1 }}
        >
          {title}
        </Typography>
        {username && (
          <Typography color="inherit" noWrap sx={{ mr: 1 }}>
            Welcome, {username}!
          </Typography>
        )}
        {children}
        <SignInOutButton hasSignIn={hasSignIn} />
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
