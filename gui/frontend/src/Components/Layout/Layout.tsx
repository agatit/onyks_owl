import React from "react";

import classes from "./Layout.module.css";

function Layout(props: any) {
  return <div className={classes.layout}>{props.children}</div>;
}

export default Layout;
