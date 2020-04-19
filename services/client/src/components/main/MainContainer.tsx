import React, { ComponentClass, FunctionComponent } from "react";
import Sidebar from "../sidebar/Sidebar";
import "./MainContainer.scss";

type Component = FunctionComponent<any> | ComponentClass<any>;

const withMainContainer = (Comp: Component) => (props: any) => {
  return (
    <div className="container">
      <div className="sidebar_container">
        <Sidebar />
      </div>
      <div className="main_container">
        <Comp {...props} />
      </div>
    </div>
  );
};

export default withMainContainer;
