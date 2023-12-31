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
  const { doSignIn } = useAuth();
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
        return errors;
      }}
      onSubmit={(values, { setSubmitting, resetForm }) => {
        doSignIn(values.username, values.password)
          .then(() => {
            onClose();
            enqueueSnackbar("Signed in successfully.", {
              variant: "success",
            });
          })
          .catch(() =>
            enqueueSnackbar("Incorrect username or password", {
              variant: "error",
            })
          )
          .finally(() => {
            setSubmitting(false);
            resetForm();
          });
      }}
    >
      {({
        values,
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
            value={values.username}
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
            hasError={touched.password && !!errors.password}
            errorMessage={errors.password}
            value={values.password}
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
            Sign in
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
      <Typography mr={1}>Don&apos;t have an account?</Typography>
      <Link onClick={onSwitch} sx={{ cursor: "pointer" }}>
        Sign up
      </Link>
    </>
  );
}

function SignInDialog(props) {
  const { open, onClose, onSwitch } = props;

  return (
    <DialogLayout
      title="Sign in"
      open={open}
      form={<Form onClose={onClose} />}
      actions={<Action onSwitch={onSwitch} />}
    />
  );
}

export default SignInDialog;
