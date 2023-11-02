import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";

function FormField(props) {
  const {
    required,
    id,
    label,
    name,
    type,
    autoComplete,
    hasError,
    errorMessage,
    value,
    handleChange,
    handleBlur,
    multiline
  } = props;
  return (
    <Grid item xs={12}>
      <TextField
        required={required}
        fullWidth
        id={id}
        label={label}
        name={name}
        type={type}
        value={value}
        autoComplete={autoComplete}
        onChange={handleChange}
        onBlur={handleBlur}
        error={hasError}
        multiline={multiline}
        rows={4}
      />
      <FormHelperText error={hasError}>
        {hasError && errorMessage}
      </FormHelperText>
    </Grid>
  );
}

export default FormField;
