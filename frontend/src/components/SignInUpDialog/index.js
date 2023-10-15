import React from "react";
import { enqueueSnackbar } from "notistack";
import SignInDialog from "./SignInDialog";
import SignUpDialog from "./SignUpDialog";

function SignInUpDialog() {
  const [openSignUp, setOpenSignUp] = React.useState(false);
  const toggleSignUp = () => setOpenSignUp(!openSignUp);
  const [openSignIn, setOpenSignIn] = React.useState(false);
  const toggleSignIn = () => setOpenSignIn(!openSignIn);
  const switchSignUpIn = () => {
    toggleSignIn();
    toggleSignUp();
  };

  React.useEffect(() => {
    setOpenSignIn(true);
    enqueueSnackbar("Please sign in first", { variant: "info" });
  }, []);

  return (
    <>
      <SignUpDialog
        open={openSignUp}
        onClose={toggleSignUp}
        onSwitch={switchSignUpIn}
      />
      <SignInDialog
        open={openSignIn}
        onClose={toggleSignIn}
        onSwitch={switchSignUpIn}
      />
    </>
  );
}

export default SignInUpDialog;
