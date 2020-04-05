import * as React from "react";
import { Route, Switch } from "react-router-dom";
// import Home from "./home";
import Page404 from "./components/error/Page404";
import OldApp from "./OldApp";
import Home from "./components/home/Home";
import D3 from "./components/d3/D3";
import Line from "./components/d3/Line";
import BarChart from "./components/d3/BarChart";

const Routes = (): JSX.Element => {
  return (
    <Switch>
      <Route exact path="/" component={Home} />
      <Route exact path="/old" component={OldApp} />
      <Route exact path="/bravo" component={BarChart} />
      {/* <Route exact path="/charlie" component={Line} /> */}
      <Route exact path="/d3" component={D3} />
      <Route component={Page404} />
    </Switch>
  );
};

export default Routes;