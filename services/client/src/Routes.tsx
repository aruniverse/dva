import * as React from "react";
import { Route, Switch } from "react-router-dom";
import Page404 from "./components/error/Page404";
import Home from "./components/home/Home";
import InidicatorPage from "./components/ui/InidicatorPage";
import StrategiesPage from "./components/ui/StrategiesPage";

const Routes = (): JSX.Element => {
  return (
    <Switch>
      <Route exact path="/" component={Home} />
      <Route exact path="/home" component={Home} />
      <Route exact path="/indicators" component={InidicatorPage} />
      <Route exact path="/strategies" component={StrategiesPage} />
      <Route component={Page404} />
    </Switch>
  );
};

export default Routes;
