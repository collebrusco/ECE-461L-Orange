import React from "react";
import { enqueueSnackbar } from "notistack";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

export default function HardwareInfo(props) {
  const [availability, setAvailability] = React.useState(props.availability);
  const [quantity, setQuantity] = React.useState(null);

  React.useEffect(() => {
    if (props.disabled) {
      setQuantity(null);
    }
  }, [setQuantity, props.disabled]);

  const handleCheckOut = () => {
    if (quantity == null || quantity <= 0) {
      return;
    }
    if (quantity > availability) {
      enqueueSnackbar("Too many to check out.", { variant: "error" });
      return;
    }
    setAvailability(availability - quantity);
  };

  const handleCheckIn = () => {
    if (quantity == null || quantity <= 0) {
      return;
    }
    if (quantity > props.capacity - availability) {
      enqueueSnackbar("Too many to check in.", { variant: "error" });
      return;
    }
    setAvailability(availability + quantity);
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
          {props.name}: {availability}/{props.capacity}
        </Typography>
      </Box>
      <TextField
        placeholder="Enter quantity"
        variant="standard"
        sx={{ p: 1 }}
        value={quantity == null ? "" : quantity}
        disabled={props.disabled}
        onChange={onQuantityChange}
      />
      <Button
        // color="info"
        variant="contained"
        disabled={props.disabled}
        onClick={handleCheckOut}
      >
        Check out
      </Button>
      <Button
        color="neutral"
        variant="contained"
        disabled={props.disabled}
        onClick={handleCheckIn}
      >
        Check in
      </Button>
    </Box>
  );
}
