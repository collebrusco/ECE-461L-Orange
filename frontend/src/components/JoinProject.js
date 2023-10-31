import React from "react";
import { Formik } from "formik";
import { enqueueSnackbar } from "notistack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import FormField from "./FormField";
import { useStore } from "./StoreProvider";

function JoinProject() {
  const { joinProject } = useStore();
  return (
    <Formik
      initialValues={{ projectName: "" }}
      validate={(values) => {
        const errors = {};
        if (!values.projectName) {
          errors.projectName = "Required";
        }
        return errors;
      }}
      onSubmit={(values, { setSubmitting, resetForm }) => {
        joinProject(values.projectName)
        .then(() => {
          enqueueSnackbar("Joined successfully.", {
            variant: "success",
          });
          resetForm();
        })
        .catch(() => {
          enqueueSnackbar("Failed to join project.", {
            variant: "error",
          });
        })
        .finally(() => {
          setSubmitting(false);
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
          width="45%"
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(e);
          }}
          noValidate
          display="flex"
          flexDirection="column"
          gap={1}
        >
          <Typography fontWeight="bold">Join project</Typography>
          <FormField
            required
            id="join-project-name"
            name="projectName"
            label="Project name"
            type="text"
            hasError={touched.projectName && !!errors.projectName}
            errorMessage={errors.projectName}
            value={values.projectName}
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
            variant="contained"
            sx={{ alignSelf: "start" }}
          >
            Join
          </Button>
        </Box>
      )}
    </Formik>
  );
}

export default JoinProject;
