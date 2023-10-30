import React from "react";
import { Formik } from "formik";
import { enqueueSnackbar } from "notistack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import FormField from "./FormField";
import { joinProject } from "../lib/api";

function JoinProject() {
  return (
    <Formik
      initialValues={{ projectID: "" }}
      validate={(values) => {
        const errors = {};
        if (!values.projectID) {
          errors.projectID = "Required";
        }
        return errors;
      }}
      onSubmit={(values, { setSubmitting }) => {
        joinProject(values.projectID)
        .then(() => {
          enqueueSnackbar("Joined successfully.", {
            variant: "success",
          });
          setTimeout(() => document.location.reload(), 1000);
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
            id="project-id"
            name="projectID"
            label="Project ID"
            type="number"
            hasError={touched.projectID && !!errors.projectID}
            errorMessage={errors.projectID}
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
