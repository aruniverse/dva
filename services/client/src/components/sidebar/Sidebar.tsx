import React from "react";
import Drawer from "@material-ui/core/Drawer";
import { List, ListItem, ListItemText } from "@material-ui/core";
import { NavLink } from "react-router-dom";
import "./Sidebar.scss";

const Sidebar = () => {
  const PageTabName = [
    "Home",
    "Form",
    "Charts",
    "Old",
    "Indicators",
    "Strategies",
  ];
  const PageTabRoute = ["/", "form", "charts", "old"];

  return (
    <Drawer open variant="permanent" anchor="left" className="Sidebar">
      <List>
        {PageTabName.map((text, index) => (
          <NavLink to={PageTabRoute[index] ?? text}>
            <ListItem button key={text}>
              <ListItemText primary={text} />
            </ListItem>
          </NavLink>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
