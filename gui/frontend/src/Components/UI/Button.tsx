import classes from "./Button.module.css";

interface BtnProps {
  color?: string;
  action: () => void;
  text: string;
}

function Button(props: BtnProps) {
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
