import React from "react";
import { useNavigate } from "react-router-dom";
import Toolbar from "@mui/material/Toolbar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import DashboardIcon from "@mui/icons-material/Dashboard";
import SignUpDialog from "../components/SignUpDialog";
import SignInDialog from "../components/SignInDialog";
import SignOutDialog from "../components/SignOutDialog";
import { authStatus, useAuth } from "../components/AuthProvider";
import TopBar from "../components/TopBar";
// import LogoutDialog from '../components/LogoutDialog';
// import NameEditDialog from '../components/NameEditDialog';
// import PasswordResetDialog from '../components/PasswordResetDialog';
// import { getProfile } from '../utils/api';

function ResourceButton({ onClick }) {
  return (
    <IconButton title="Resource Management" color="inherit" onClick={onClick}>
      <DashboardIcon />
    </IconButton>
  );
}

function SignInOutButton({ hasSignIn, handleSignIn, handleSignOut }) {
  const title = hasSignIn ? "Sign Out" : "Sign In";
  const onClick = hasSignIn ? handleSignOut : handleSignIn;
  return (
    <IconButton title={title} color="inherit" onClick={onClick}>
      {hasSignIn ? <LogoutIcon /> : <LoginIcon />}
    </IconButton>
  );
}

function Content(props) {
  // const { username } = props;
  const [username, setUsername] = React.useState("");

  React.useEffect(() => {
    setUsername(localStorage.getItem("currentUser") || "null");
  }, []);

  return (
    <Grid container display="flex" alignItems="center" rowSpacing={2}>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center" gap={1}>
          <Typography fontWeight="bold">Username</Typography>
          <Typography>{username}</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center" gap={1}>
          <Typography fontWeight="bold">Field</Typography>
          <Typography>placeholder</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center" gap={1}>
          <Typography fontWeight="bold">Field</Typography>
          <Typography>placeholder</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center" gap={1}>
          <Typography fontWeight="bold">Field</Typography>
          <Typography>placeholder</Typography>
        </Box>
      </Grid>
      <Grid item xs={12}>
        <Button
          fullWidth
          variant="outlined"
          onClick={() => alert('clicked!')}
        >
          Some Button
        </Button>
      </Grid>
    </Grid>
  );
}

function UserManagement() {
  const navigate = useNavigate();
  const { status } = useAuth();

  const hasSignIn = status === authStatus.authenticated;

  // Dialog states
  const [openSignUp, setOpenSignUp] = React.useState(false);
  const toggleSignUp = () => setOpenSignUp(!openSignUp);
  const [openSignIn, setOpenSignIn] = React.useState(false);
  const toggleSignIn = () => setOpenSignIn(!openSignIn);
  const [openSignOut, setOpenSignOut] = React.useState(false);
  const toggleSignOut = () => setOpenSignOut(!openSignOut);
  const switchSignUpIn = () => {
    toggleSignIn();
    toggleSignUp();
  };

  // const [profile, setProfile] = React.useState({
  //   name: null,
  //   email: null,
  // });

  // const update = () => {
  //   getProfile()
  //     .then(setProfile)
  //     .catch((error) => {
  //       enqueueSnackbar(error.message, { variant: 'error' });
  //     });
  // };

  React.useEffect(() => {
    document.title = "User Management";
    setOpenSignIn(!hasSignIn);
  }, [hasSignIn]);

  return (
    <>
      {/* Dialogs */}
      <SignUpDialog open={openSignUp} onClose={toggleSignUp} onSwitch={switchSignUpIn} />
      <SignInDialog open={openSignIn} onClose={toggleSignIn} onSwitch={switchSignUpIn} />
      <SignOutDialog open={openSignOut} onClose={toggleSignOut} />

      {/* Main component */}
      <Box sx={{ display: "flex" }}>
        {/* TopBar */}
        <TopBar
          title="User Management"
          buttons={
            <>
              <ResourceButton onClick={() => navigate("/resource")} />
              <SignInOutButton
                hasSignIn={hasSignIn}
                handleSignIn={toggleSignIn}
                handleSignOut={toggleSignOut}
              />
            </>
          }
        />

        <Box
          component="main"
          sx={{
            backgroundColor: "#f5f5f5",
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Toolbar />
          <Container maxWidth="md" sx={{ mt: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 4, display: "flex" }}>
                  <Content
                    username="placeholder"
                  />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Box>
    </>
  );
}

export default UserManagement;
