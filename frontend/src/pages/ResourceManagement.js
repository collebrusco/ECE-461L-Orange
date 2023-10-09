import * as React from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import Link from '@mui/material/Link';

function TopBar(props) {
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
          Resource Management
        </Typography>
        <IconButton
          title="Profile"
          color="inherit"
          onClick={props.handleProfile}
        >
          <AccountBoxIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}

TopBar.propTypes = {
  handleProfile: PropTypes.func,
};

function Content() {
  return (
    <>
      {/* Title */}
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Title
        {/* Recent Deposits */}
      </Typography>

      <Typography component="p" variant="h4">
        Content
        {/* $3,024.00 */}
      </Typography>

      <Typography color="text.secondary" sx={{ flex: 1 }}>
        Date
        {/* on 15 March, 2019 */}
      </Typography>

      <div>
        <Link color="primary" href="https://google.com/">
          View balance
        </Link>
      </div>

    </>
  );
}

function ResourceManagement() {
  const navigate = useNavigate();

  React.useEffect(() => {
    document.title = 'Resource Management';
  }, []);

  return (
    <Box sx={{ display: 'flex' }}>

      {/* TopBar */}
      <TopBar
        handleProfile={() => navigate('/profile')}
      />

      {/* Content */}
      <Box
        component="main"
        sx={{
          backgroundColor: (theme) => (
            theme.palette.mode === 'light'
              ? theme.palette.grey[100]
              : theme.palette.grey[900]),
          flexGrow: 1,
          height: '100vh',
          overflow: 'auto',
        }}
      >
        <Toolbar />
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 240,
                }}
              >
                <Content />
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>

    </Box>
  );
}

export default ResourceManagement;
