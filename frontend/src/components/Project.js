import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import HardwareInfo from "./HardwareInfo";
import { projectsInfo } from "../lib/data";
import { useAuth } from "./AuthProvider";

export default function Project(props) {
  const { name } = props;
  const projectInfo = projectsInfo[name];
  const { user } = useAuth();

  const members = [...projectInfo.members, user];
  return (
    <Box
      display="flex"
      alignItems="center"
    >
      <Box flexGrow={1}>
        <Typography component="h2" variant="h6">
          {name}
        </Typography>
        <Typography>{members.join(", ")}</Typography>
      </Box>
      <Box>
        <Box>
          {projectInfo.hardwares.map((hardware) => (
            <HardwareInfo
              name={hardware.name}
              availability={hardware.availability}
              capacity={hardware.capacity}
            />
          ))}
        </Box>
      </Box>
    </Box>
  );
}
