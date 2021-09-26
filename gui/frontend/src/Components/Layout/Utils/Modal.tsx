import classes from "./Modal.module.css";

interface ModalProps {
  text: string;
  inputFlag?: boolean;
  children?: any;
}

function Modal(props: ModalProps) {
  return (
    <div className={classes.modal}>
      {props.text}
      {props.children}
    </div>
  );
}
export default Modal;
