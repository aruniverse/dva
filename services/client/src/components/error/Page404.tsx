import * as React from "react";
import withMainContainer from "../main/MainContainer";

const Page404 = () => {
  return (
    <div className="error-pg-404">
      <h1>Error 404:</h1>
      <h3>The page you requested does not exist</h3>
    </div>
  );
};

export default withMainContainer(Page404);
