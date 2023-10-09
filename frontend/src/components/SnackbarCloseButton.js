import React from "react";
import { useSnackbar } from "notistack";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

function SnackbarCloseButton(props) {
  const { closeSnackbar } = useSnackbar();
  return (
    <IconButton onClick={() => closeSnackbar(props.key)}>
      <CloseIcon htmlColor="#fff" />
    </IconButton>
  );
}

export default SnackbarCloseButton;
