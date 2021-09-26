import Logo from "./Logo";
import Button from "../Components/UI/Button";

import classes from "./StarterPage.module.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import Modal from "../Components/Layout/Utils/Modal";
import Backdrop from "../Components/Layout/Utils/Backdrop";

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
              <Link to="/edit">
                <Button text="Testowy projekt" action={() => {}} />
              </Link>
            </li>
          </ul>
          <div className={classes.createPrjBtn}>
            <Button text="Stwórz projekt" action={openModalHandler} />
          </div>
        </div>
      </div>
      {modalIsOpen && (
        <Modal text="Wprowadź nazwę projektu:" inputFlag={true}>
          <div>
            <input type="text" />
          </div>
          <Link to="/edit">
            <Button text="Zatwierdź" action={closeModalHandler} />
          </Link>
        </Modal>
      )}
      {modalIsOpen && <Backdrop action={closeModalHandler} />}
    </div>
  );
}

export default StarterPage;
