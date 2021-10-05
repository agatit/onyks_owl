import Logo from "./Logo";
import { Button } from "react-bootstrap";
import classes from "./StarterPage.module.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import Modal from "../Components/Layout/Utils/Modal";
import Backdrop from "../Components/Layout/Utils/Backdrop";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit } from "@fortawesome/free-solid-svg-icons";

function StarterPage() {
  const [modalIsOpen, setModalOpen] = useState(false);

  function openModalHandler() {
    setModalOpen(true);
  }

  function closeModalHandler() {
    setModalOpen(false);
  }

  return (
    <div className={classes.starter}>
      <div className={classes.bgimg}>
        <div className={classes.title}>
          <h1>Onyks owl </h1>
        </div>
        <div className={classes.logo}>
          <Logo />
        </div>
        <div className={classes.menu}>
          <h4>Wybierz projekt lub utwórz nowy!</h4>
          <ul>
            <li>
              <Link to="/player">
                <Button variant="dark">Testowy projekt</Button>
              </Link>
              <Link to="/edit" style={{ textDecoration: "none" }}>
                <span>
                  <FontAwesomeIcon icon={faEdit} size="lg" />
                </span>
              </Link>
            </li>
          </ul>
          <div className={classes.createPrjBtn}>
            <Button onClick={openModalHandler}>Stwórz projekt</Button>
          </div>
        </div>
      </div>
      {modalIsOpen && (
        <Modal text="Wprowadź nazwę projektu:" inputFlag={true}>
          <div>
            <input type="text" />
          </div>
          <Link to="/edit">
            <Button onClick={closeModalHandler}>Zatwierdź </Button>
          </Link>
        </Modal>
      )}
      {modalIsOpen && <Backdrop action={closeModalHandler} />}
    </div>
  );
}

export default StarterPage;
