import Logo from "./Logo";
import { Button } from "react-bootstrap";
import classes from "./StarterPage.module.css";
import { Link } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import Modal from "../Components/Layout/Utils/Modal";
import Backdrop from "../Components/Layout/Utils/Backdrop";
import { Project } from "../store/redux-query/models/Project";
import { useRequest } from "redux-query-react";
import {
  addProject,
  listProjects,
} from "../store/redux-query/apis/ProjectManagementApi";
import ProjectList from "../Components/UI/Menu-UI/ProjectList";
import { QueryConfig, requestAsync } from "redux-query";
import store from "../store/store";
import { useSelector } from "react-redux";
import * as projectSelectors from "../store/selectors/projectSelectors";

export const createRequestMaker = (name: string) => {
  const newPrj: any = {
    project: { id: name, comment: "he he" },
  };
  return requestAsync(addProject(newPrj));
};

function StarterPage() {
  const [modalIsOpen, setModalOpen] = useState(false);

  const createPrjInputRef = useRef<HTMLInputElement>(null);

  const obj: QueryConfig = {
    url: "",
    transform: (response: any) => {
      console.log(response);
      return {
        projects: response,
      };
    },
    update: {
      projects: (prevVal, newVal) => newVal,
    },
  };

  const [{ isPending, status }, refresh] = useRequest(listProjects(obj));

  function openModalHandler() {
    setModalOpen(true);
  }

  function closeModalHandler() {
    setModalOpen(false);
  }

  function createPrjBtnHandler() {
    const prjName = createPrjInputRef.current!.value;
    store.dispatch(createRequestMaker(prjName));
    setModalOpen(false);
  }

  const projects = useSelector(projectSelectors.getProjectList);

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
          {isPending ? <Backdrop /> : <ProjectList projects={projects} />}
        </div>
        <div className={classes.createPrjBtn}>
          <Button onClick={openModalHandler}>Stwórz projekt</Button>
        </div>
      </div>
      {modalIsOpen && (
        <Modal text="Wprowadź nazwę projektu:" inputFlag={true}>
          <div>
            <input type="text" ref={createPrjInputRef} />
          </div>
          <Link to="/edit">
            <Button onClick={createPrjBtnHandler}>Zatwierdź </Button>
          </Link>
        </Modal>
      )}
      {modalIsOpen && <Backdrop action={closeModalHandler} />}
    </div>
  );
}

export default StarterPage;
