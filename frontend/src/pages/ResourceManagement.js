import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import IconButton from '@mui/material/IconButton';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import Layout from "./Layout";
import Project from "../components/Project";
import HardwareInfo from '../components/HardwareInfo';
import { getResources, getUserProjects } from "../lib/api";

function Resources() {
  const [resources, setResources] = React.useState([]);

  React.useEffect(() => {
    getResources().then(setResources);
  }, []);

  return (
    <Box display="flex" justifyContent="space-around" p={2}>
      {
        resources.map(resource => (
          <HardwareInfo
            name={resource.title}
            capacity={resource.capacity}
            availability={resource.availability}
          />
        ))
      }
    </Box>
  );
}

function Projects() {
  const [projects, setProjects] = React.useState([]);

  React.useEffect(() => {
    getUserProjects().then(setProjects);
  }, []);

  return (
    <Box display="flex" flexDirection="column" gap={2} mt={2} mb={2} >
      {projects.map(project => (
        <Project
          name={project.title}
          description={project.description}
          members={project.users}
          hardwares={project.resources}
        />
      ))}
    </Box>
  );
}

function ResourceManagement() {
  const navigate = useNavigate();

  return (
    <Layout
      title="Resource Management"
      buttons={
        <IconButton
          title="User Management"
          color="inherit"
          onClick={() => navigate("/user")}
        >
          <AccountBoxIcon />
        </IconButton>
      }
    >
      <Paper
        sx={{
          maxWidth: "55%",
          m: "auto",
          mt: 4,
          p: 4,
        }}
      >
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
          Resources
        </Typography>
        <Resources />
      </Paper>
      <Paper
        sx={{
          maxWidth: "55%",
          m: "auto",
          mt: 4,
          p: 4,
        }}
      >
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
          Project Usages
        </Typography>
        <Projects />
      </Paper>
    </Layout>
  );
}

export default ResourceManagement;
