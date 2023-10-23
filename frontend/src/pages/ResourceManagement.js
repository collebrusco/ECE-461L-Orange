import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import IconButton from '@mui/material/IconButton';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import Layout from "./Layout";
import Project from "../components/Project";
import { projectNames } from "../lib/data";

function Content() {
  return (
    <Box display="flex" flexDirection="column" gap={2} mt={2} mb={2} >
      {projectNames.map(name => (
        <Project name={name} />
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
        <Content />
      </Paper>
    </Layout>
  );
}

export default ResourceManagement;
