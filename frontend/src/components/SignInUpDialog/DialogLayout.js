import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import Avatar from "@mui/material/Avatar";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

function DialogLayout(props) {
  const { title, open, form, actions } = props;
  return (
    <Dialog open={open}>
      <Box
        sx={{
          m: "auto",
          mt: 4,
          width: "80%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          {title}
        </Typography>
        {form}
      </Box>
      <DialogActions sx={{ p: 2, pt: 0 }}>{actions}</DialogActions>
    </Dialog>
  );
}

export default DialogLayout;
