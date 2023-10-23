import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

function CreateProject() {
  return (
    <Box display="flex" flexDirection="column" gap={1}>
      <Typography fontWeight="bold">Create new project</Typography>
      <TextField required label="Name" fullWidth />
      <TextField label="Description" multiline rows={4} fullWidth />
      <Button variant="contained" sx={{ alignSelf: "start" }}>
        Submit
      </Button>
    </Box>
  );
}

export default CreateProject;
