import React from "react";
import { ReactComponent as Logo } from "./logo.svg";
import "./App.css";
import { Helmet } from "react-helmet";
import withMainContainer from "./components/main/MainContainer";

const OldApp: React.FC = () => {
  return (
    <div className="App">
      <Helmet>{"old app"}</Helmet>
      <header className="App-header">
        <Logo className="App-logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
};

export default withMainContainer(OldApp);
