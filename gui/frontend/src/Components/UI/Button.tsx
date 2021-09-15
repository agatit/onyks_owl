import React from "react";

import classes from "./Button.module.css";

function Button(props: any) {
  return (
    <button
      color={props.color}
      onClick={props.action}
      className={classes.toolsButton}
    >
      {props.text}
    </button>
  );
}

export default Button;
