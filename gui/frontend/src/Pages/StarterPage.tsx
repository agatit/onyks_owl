import { useState } from "react";
import { Button, Stack } from "react-bootstrap";
import Backdrop from "../Components/Layout/Utils/Backdrop";
import CreateProjectForm from "../Components/UI/CreateProjectForm";
import ProjectList from "../Components/UI/Menu-UI/ProjectList";
import StarterFooter from "../Components/UI/StarterFooter";
import StarterNavbar from "../Components/UI/StarterNavbar";

function StarterPage() {
  const [modalIsOpen, setModalOpen] = useState(false);

  function openModalHandler() {
    setModalOpen(true);
  }

  function closeModalHandler() {
    setModalOpen(false);
  }

  return (
    <Stack gap={3} style={stackStyle}>
      <StarterNavbar />
      <ProjectList />
      <StarterFooter>
        <Button variant="success" onClick={openModalHandler}>
          Stwórz projekt
        </Button>
      </StarterFooter>
      {modalIsOpen && <CreateProjectForm closeModalFunc={closeModalHandler} />}
      {modalIsOpen && <Backdrop action={closeModalHandler} />}
    </Stack>
  );
}

export default StarterPage;

const stackStyle = {
  backgroundColor: "rgb(180,180,180)",
};
