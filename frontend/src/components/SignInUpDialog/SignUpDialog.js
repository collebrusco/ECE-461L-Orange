import { enqueueSnackbar } from "notistack";
import { Formik } from "formik";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Link from "@mui/material/Link";
import DialogLayout from "./DialogLayout";
import FormField from "../FormField";
import { useAuth } from "../AuthProvider.js";

function Form(props) {
  const { onClose } = props;
  const { doSignUp } = useAuth();
  return (
    <Formik
      initialValues={{ username: "", password: "" }}
      validate={(values) => {
        const errors = {};
        if (!values.username) {
          errors.username = "Required";
        }
        if (!values.password) {
          errors.password = "Required";
        }
        if (!values.confirmPassword) {
          errors.confirmPassword = "Required";
        } else if (values.password !== values.confirmPassword) {
          errors.confirmPassword = "Passwords didn't match. Try again.";
        }
        return errors;
      }}
      onSubmit={(values, { setSubmitting }) => {
        doSignUp(values.username, values.password).then((ok) => {
          if (ok) {
            onClose();
            enqueueSnackbar("Signed up successfully.", {
              variant: "success",
            });
          } else {
            enqueueSnackbar("Cannot sign up.", { variant: "error" });
          }
          setSubmitting(false);
          setTimeout(() => document.location.reload(), 1000);
        });
      }}
    >
      {({
        errors,
        touched,
        handleChange,
        handleBlur,
        handleSubmit,
        isSubmitting,
      }) => (
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(e);
          }}
          noValidate
          p={3}
          width="25vw"
          display="flex"
          flexDirection="column"
          gap={2}
        >
          {/* Username */}
          <FormField
            required
            id="username"
            label="Username"
            name="username"
            type="text"
            autoComplete="username"
            hasError={touched.username && !!errors.username}
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
            autoComplete="new-password"
            hasError={touched.password && !!errors.password}
            errorMessage={errors.password}
            handleChange={handleChange}
            handleBlur={handleBlur}
          />
          {/* Confirm Password */}
          <FormField
            required
            id="confirmPassword"
            label="Confirm password"
            name="confirmPassword"
            type="password"
            hasError={touched.confirmPassword && !!errors.confirmPassword}
            errorMessage={errors.confirmPassword}
            handleChange={handleChange}
            handleBlur={handleBlur}
          />
          <Button
            type="submit"
            onClick={() => {
              if (!Object.values(errors).every((v) => v === "")) {
                enqueueSnackbar("Please resolve the error and try again.", {
                  variant: "error",
                });
              }
            }}
            disabled={isSubmitting}
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign up
          </Button>
        </Box>
      )}
    </Formik>
  );
}

function Action(props) {
  const { onSwitch } = props;
  return (
    <>
      <Typography mr={1}>Already have an account?</Typography>
      <Link onClick={onSwitch} sx={{ cursor: "pointer" }}>
        Sign in
      </Link>
    </>
  );
}

function SignUpDialog(props) {
  const { open, onClose, onSwitch } = props;

  return (
    <DialogLayout
      title="Sign up"
      open={open}
      form={<Form onClose={onClose} />}
      actions={<Action onSwitch={onSwitch} />}
    />
  );
}

export default SignUpDialog;
