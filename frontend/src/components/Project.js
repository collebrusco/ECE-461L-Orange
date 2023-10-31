import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import HardwareUsage from "./HardwareUsage";

export default function Project(props) {
  const { name, description, members, hardwares } = props;

  return (
    <Box display="flex" alignItems="center">
      <Box flexGrow={1}>
        <Typography component="h2" variant="h6">
          {name}
        </Typography>
        <Typography>Members: {members.join(", ")}</Typography>
        <Typography>Description: {description}</Typography>
      </Box>
      <Box>
        <Box>
          {Object.keys(hardwares).map((hardware_name) => (
            <HardwareUsage
              name={hardware_name}
              usage={hardwares[hardware_name]}
              projectName={name}
            />
          ))}
        </Box>
      </Box>
    </Box>
  );
}
