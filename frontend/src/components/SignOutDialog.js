import { useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import { useAuth } from "./AuthProvider";

function SignOutDialog(props) {
  const { open, onClose } = props;
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const { doSignOut } = useAuth();
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle id="alert-dialog-title">Sign out</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Are you sure you want to sign out?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>No</Button>
        <Button
          onClick={() =>
            doSignOut().then(() => {
              onClose();
              enqueueSnackbar("Signed out successfully.", {
                variant: "success",
              });
              setTimeout(() => navigate(0), 1000);
            })
          }
          autoFocus
          variant="contained"
        >
          Yes
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default SignOutDialog;
