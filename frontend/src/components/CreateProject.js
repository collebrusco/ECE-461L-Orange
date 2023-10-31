import React from "react";
import { Formik } from "formik";
import { enqueueSnackbar } from "notistack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import FormField from "./FormField";
import { useStore } from "./StoreProvider";

function CreateProject() {
  const { createProject } = useStore();
  return (
    <Formik
      initialValues={{ name: "", description: "" }}
      validate={(values) => {
        const errors = {};
        if (!values.name) {
          errors.name = "Required";
        }
        return errors;
      }}
      onSubmit={(values, { setSubmitting, resetForm }) => {
        createProject(values.name, values.description)
          .then(() => {
            enqueueSnackbar("Create project successfully.", {
              variant: "success",
            });
            resetForm();
          })
          .catch(() => {
            enqueueSnackbar("Failed to create project.", {
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
          <Typography fontWeight="bold">Create new project</Typography>
          <FormField
            required
            id="create-project-name"
            name="name"
            label="Name"
            type="text"
            hasError={touched.name && !!errors.name}
            errorMessage={errors.name}
            value={values.name}
            handleChange={handleChange}
            handleBlur={handleBlur}
          />
          <FormField
            required
            id="project-description"
            name="description"
            label="Description"
            hasError={touched.description && !!errors.description}
            errorMessage={errors.description}
            value={values.description}
            handleChange={handleChange}
            handleBlur={handleBlur}
            multiline
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
            Create
          </Button>
        </Box>
      )}
    </Formik>
  );
}

export default CreateProject;
