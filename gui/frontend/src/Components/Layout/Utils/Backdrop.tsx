import classes from "./Backdrop.module.css";

function Backdrop(props: any) {
  return <div className={classes.backdrop} onClick={props.action} />;
}

export default Backdrop;
