import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import HardwareInfo from "./HardwareInfo";

export default function Project(props) {
  const { name, description, members, hardwares } = props;

  return (
    <Box
      display="flex"
      alignItems="center"
    >
      <Box flexGrow={1}>
        <Typography component="h2" variant="h6">
          {name}
        </Typography>
        <Typography>Members: {members.join(", ")}</Typography>
        <Typography>Description: {description}</Typography>
      </Box>
      <Box>
        <Box>
          {hardwares.map((hardware) => {
            const name = Object.keys(hardware)[0];
            const availability = hardware[name];
            return (
              <HardwareInfo
                name={name}
                availability={availability}
                capacity={100}
              />
            );
          })}
        </Box>
      </Box>
    </Box>
  );
}
