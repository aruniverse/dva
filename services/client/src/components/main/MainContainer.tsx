import React, { ComponentClass, FunctionComponent } from "react";
import Sidebar from "../sidebar/Sidebar";
import "./MainContainer.scss";

type Component = FunctionComponent<any> | ComponentClass<any>;

const withMainContainer = (Comp: Component) => (props: any) => {
  return (
    <div className="container">
      <div className="sidebar_wrapper">
        <div className="sidebar_container">
          <Sidebar />
        </div>
        <div className="main_wrapper">
          <div className="main_content">
            <Comp {...props} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default withMainContainer;
