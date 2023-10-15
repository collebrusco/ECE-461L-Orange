import React from "react";
import IconButton from "@mui/material/IconButton";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import SignOutDialog from "./SignOutDialog";

function SignInOutButton(props) {
  const { hasSignIn } = props;
  const [open, setOpen] = React.useState(false);
  const toggleOpen = () => setOpen(open => !open);
  const title = hasSignIn ? "Sign Out" : "Sign In";
  const onClick = hasSignIn ? toggleOpen : null;

  return (
    <>
      <SignOutDialog open={open} onClose={toggleOpen} />
      <IconButton title={title} color="inherit" onClick={onClick}>
        {hasSignIn ? <LogoutIcon /> : <LoginIcon />}
      </IconButton>
    </>
  );
}

export default SignInOutButton;
