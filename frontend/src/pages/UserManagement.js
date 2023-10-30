import React from "react";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import DashboardIcon from "@mui/icons-material/Dashboard";
import { useAuth } from "../components/AuthProvider";
import CreateProject from "../components/CreateProject";
import JoinProject from "../components/JoinProject";
import { getUserProjects } from "../lib/api";
import Layout from "./Layout";

function ProjectInfo(props) {
  const { name, isCreator } = props;
  return (
    <Grid container>
      <Grid item xs={6}>
        <Typography>{name}</Typography>
      </Grid>
      <Grid item xs={6}>
        <Typography>{isCreator ? "Owner" : "Member"}</Typography>
      </Grid>
    </Grid>
  );
}

function Content() {
  const { user } = useAuth();
  const joinedDate = format(new Date(), "MMMM d, yyyy");
  const [projects, setProjects] = React.useState([]);

  React.useEffect(() => {
    getUserProjects().then(setProjects);
  }, []);

  return (
    <Box width="80%" m="auto" display="flex" flexDirection="column">
      <Grid container>
        <Grid item xs={6}>
          <Typography fontWeight="bold">Username</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>{user}</Typography>
        </Grid>
      </Grid>
      <Grid container>
        <Grid item xs={6}>
          <Typography fontWeight="bold">Joined on</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>{joinedDate}</Typography>
        </Grid>
      </Grid>
      <Box mt={2}>
        <Typography fontWeight="bold">Project list</Typography>
        <Box mt={1}>
          {projects.map(({title, creator}) => (
            <ProjectInfo name={title} isCreator={user === creator} />
          ))}
        </Box>
      </Box>
      <Box mt={2} display="flex" justifyContent="space-between">
        <CreateProject />
        <JoinProject />
      </Box>
    </Box>
  );
}

function UserManagement() {
  const navigate = useNavigate();

  return (
    <Layout
      title="User Management"
      buttons={
        <IconButton
          title="Resource Management"
          color="inherit"
          onClick={() => navigate("/resource")}
        >
          <DashboardIcon />
        </IconButton>
      }
    >
      <Paper
        sx={{
          maxWidth: "50%",
          m: "auto",
          mt: 4,
          p: 4,
        }}
      >
        <Content />
      </Paper>
    </Layout>
  );
}

export default UserManagement;
