import Logo from "./Logo";
import { Button } from "react-bootstrap";
import classes from "./StarterPage.module.css";
import { useState } from "react";
import Backdrop from "../Components/Layout/Utils/Backdrop";
import ProjectList from "../Components/UI/Menu-UI/ProjectList";
import CreateProjectForm from "../Components/UI/CreateProjectForm";
import { ToastContainer } from "react-toastify";

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
          <ProjectList />
        </div>
        <div className={classes.createPrjBtn}>
          <Button onClick={openModalHandler}>Stwórz projekt</Button>
        </div>
      </div>
      {modalIsOpen && <CreateProjectForm closeModalFunc={closeModalHandler} />}
      {modalIsOpen && <Backdrop action={closeModalHandler} />}
      <ToastContainer />
    </div>
  );
}

export default StarterPage;
