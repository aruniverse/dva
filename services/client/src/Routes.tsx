import * as React from "react";
import { Route, Switch } from "react-router-dom";
import Page404 from "./components/error/Page404";
import OldApp from "./OldApp";
import Home from "./components/home/Home";
import LoadChart from "./components/d3/SampleCode";
import Test from "./components/axioscomp/Test";
import TestData from "./components/ui/TestData";
import InidicatorPage from "./components/axioscomp/InidicatorPage";

const Routes = (): JSX.Element => {
  return (
    <Switch>
      <Route exact path="/" component={Home} />
      <Route exact path="/home" component={Home} />
      {/* <Route exact path="/old" component={OldApp} /> */}
      {/* <Route exact path="/form" component={Test} /> */}
      {/* <Route exact path="/charts" component={LoadChart} /> */}
      <Route exact path="/indicators" component={InidicatorPage} />
      <Route exact path="/strategies" component={TestData} />
      <Route component={Page404} />
    </Switch>
  );
};

export default Routes;
