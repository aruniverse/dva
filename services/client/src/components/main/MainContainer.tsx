import React, { ComponentClass, FunctionComponent } from "react";
import Sidebar from "../sidebar/Sidebar";

type Component = FunctionComponent<any> | ComponentClass<any>;

const withMainContainer = (Comp: Component) => (props: any) => {
  return (
    <div id={"container"} className="main_mainContainer">
      <div id={"content_wrapper"}>
        <div id={"header_container"}>
          <Sidebar />
        </div>
        <div id={"main_wrapper"}>
          <div id={"main_content"}>
            <Comp {...props} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default withMainContainer;
