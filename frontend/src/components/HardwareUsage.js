import React from "react";
import { enqueueSnackbar } from "notistack";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useStore } from "./StoreProvider";

export default function HardwareUsage(props) {
  const { name, usage, projectName } = props;
  const [quantity, setQuantity] = React.useState(null);
  const [availability, setAvailability] = React.useState(0);

  const { resources, checkout, checkin } = useStore();
  React.useEffect(() => {
    const resource = resources.find((resource) => resource.title === name);
    setAvailability(resource.availability);
  }, [resources, name]);

  const handleCheckOut = () => {
    if (quantity == null || quantity <= 0) {
      return;
    }
    if (quantity > availability) {
      enqueueSnackbar("Too many to check out.", { variant: "error" });
      return;
    } else {
      checkout(name, quantity, projectName);
    }
  };

  const handleCheckIn = () => {
    if (quantity == null || quantity <= 0) {
      return;
    }
    if (quantity > usage) {
      enqueueSnackbar("Too many to check in.", { variant: "error" });
      return;
    } else {
      checkin(name, quantity, projectName);
    }
  };

  const onQuantityChange = (e) => {
    if (e.target.value === "") {
      setQuantity(null);
      return;
    }
    const value = Number(e.target.value);
    if (isNaN(value)) {
      return;
    }
    setQuantity(value);
  };

  return (
    <Box display="flex" flexDirection="row" gap={1} alignItems="center">
      <Box flexGrow={1}>
        <Typography>
          {name} Usage: {usage}
        </Typography>
      </Box>
      <TextField
        placeholder="Enter quantity"
        variant="standard"
        sx={{ p: 1 }}
        value={quantity == null ? "" : quantity}
        onChange={onQuantityChange}
      />
      <Button variant="contained" onClick={handleCheckOut}>
        Check out
      </Button>
      <Button color="neutral" variant="contained" onClick={handleCheckIn}>
        Check in
      </Button>
    </Box>
  );
}
