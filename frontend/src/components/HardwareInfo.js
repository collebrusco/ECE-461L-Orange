import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import CircularProgress from "./CirularProgress";

export default function HardwareInfo(props) {
  const { name, capacity, availability } = props;
  return (
    <Box display="flex" flexDirection="column" gap={1}>
      <Typography component="h3" variant="h6" textAlign="center">
        {name}
      </Typography>
      <Box alignSelf="center">
        <CircularProgress value={(availability * 100) / capacity} />
      </Box>
      <Box width="10rem" display="flex">
        <Box width="80%">
          <Typography fontWeight="bold">Availability</Typography>
        </Box>
        <Box width="20%">
          <Typography>{availability}</Typography>
        </Box>
      </Box>
      <Box display="flex">
        <Box width="80%">
          <Typography fontWeight="bold">Capacity</Typography>
        </Box>
        <Box width="20%">
          <Typography>{capacity}</Typography>
        </Box>
      </Box>
    </Box>
  );
}
