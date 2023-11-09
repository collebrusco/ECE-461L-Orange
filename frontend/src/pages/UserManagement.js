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
import { useStore } from "../components/StoreProvider";
import CreateProject from "../components/CreateProject";
import JoinProject from "../components/JoinProject";
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
  const { user: { created_at, username } } = useAuth();
  const joinedDate = created_at && format(new Date(created_at * 1000), "MMMM d, yyyy");
  const { projects } = useStore();

  return (
    <Box width="80%" m="auto" display="flex" flexDirection="column">
      <Grid container>
        <Grid item xs={6}>
          <Typography fontWeight="bold">Username</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>{username}</Typography>
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
            <ProjectInfo name={title} isCreator={username === creator} />
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
