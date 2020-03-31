import React from "react";
import { ReactComponent as Logo } from "../../logo.svg";
import withMainContainer from "../main/MainStyle";

const Home = () => {
  return (
    <div>
      <Logo />
    </div>
  );
};

export default withMainContainer(Home);
