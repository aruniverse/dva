import React from "react";
import Drawer from "@material-ui/core/Drawer";
import { List, ListItem, ListItemIcon, ListItemText } from "@material-ui/core";
import { ReactComponent as Logo } from "../../logo.svg";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  return (
    <Drawer open variant="permanent" anchor="left">
      <List>
        {["/", "old", "alpha", "bravo", "charlie", "d3"].map(text => (
          <NavLink to={text}>
            <ListItem button key={text}>
              <ListItemIcon>
                <Logo />
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          </NavLink>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
