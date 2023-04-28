import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Button } from '@material-ui/core';
import Alerts from './components/Alerts';
import Configuration from './components/Configuration';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Food Security Alerts
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Alerts
          </Button>
          <Button color="inherit" component={Link} to="/config">
            Configuration
          </Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Switch>
          <Route path="/" exact component={Alerts} />
          <Route path="/config" component={Configuration} />
        </Switch>
      </Container>
    </Router>
  );
}

export default App;
