import React from "react";
import { Helmet } from "react-helmet";
import { Router } from "react-router";
import Routes from "./Routes";
import { createBrowserHistory } from "history";

const history = createBrowserHistory();

const App = () => {
  return (
    <div>
      <Helmet>
        <title>{"Team TBD"}</title>
      </Helmet>
      <Router history={history}>
        <Routes />
      </Router>
    </div>
  );
};

export default App;
