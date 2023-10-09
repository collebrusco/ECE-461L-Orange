import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

function TopBar(props) {
  const { title, buttons } = props;
  return (
    <AppBar position="absolute">
      <Toolbar>
        <Typography
          component="h1"
          variant="h6"
          color="inherit"
          noWrap
          sx={{ flexGrow: 1 }}
        >
          {title}
        </Typography>
        {buttons}
      </Toolbar>
    </AppBar>
  );
}

export default TopBar;
