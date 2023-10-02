import { useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";
import { useFormik } from "formik";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import FormField from "../components/FormField";
import { useAuth } from "./AuthProvider.js";

function SignInDialog(props) {
  const { open, onClose, onSwitch } = props;
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();
  const { doSignIn } = useAuth();

  const hasError = (value) => touched[value] && !!errors[value];
  const handleSubmitBtn = () => {
    if (!Object.values(errors).every((v) => v === "")) {
      enqueueSnackbar("Please resolve the error and try again.", {
        variant: "error",
      });
    }
  };
  const validate = (values) => {
    const errors = {};
    if (!values.username) {
      errors.username = "Required";
    }

    if (!values.password) {
      errors.password = "Required";
    }

    return errors;
  };
  const onSubmit = (values) => {
    doSignIn(values.username, values.password).then((ok) => {
      if (ok) {
        alert(`Username: ${values.username}\nPassword: ${values.password}\n`);
        onClose();
        enqueueSnackbar("Signed up successfully.", { variant: "success" });
        setTimeout(() => navigate(0), 1000);
      } else {
        enqueueSnackbar("Incorrect username or password", {
          variant: "error",
        });
      }
    });
  };
  const { handleSubmit, handleChange, handleBlur, touched, errors } = useFormik(
    {
      initialValues: {
        username: "",
        password: "",
      },
      validate,
      onSubmit,
    }
  );

  return (
    <Dialog open={open}>
      <Container maxWidth="xs">
        <Box
          sx={{
            // marginTop: 2,
            margin: "2em auto 0",
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
            Sign in
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              {/* Username */}
              <FormField
                required
                id="username"
                label="Username"
                name="username"
                type="username"
                autoComplete="username"
                hasError={hasError("username")}
                errorMessage={errors.username}
                handleChange={handleChange}
                handleBlur={handleBlur}
              />
              {/* Password */}
              <FormField
                required
                id="password"
                label="Password"
                name="password"
                type="password"
                autoComplete="current-password"
                hasError={hasError("password")}
                errorMessage={errors.password}
                handleChange={handleChange}
                handleBlur={handleBlur}
              />
            </Grid>
            <Button
              type="submit"
              onClick={handleSubmitBtn}
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign in
            </Button>
          </Box>
        </Box>
      </Container>
      <DialogActions>
        <Button onClick={onSwitch} variant="text">
          Don&apos;t have an account? Sign Up
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default SignInDialog;
