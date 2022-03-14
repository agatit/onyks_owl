import { FormEvent, useRef } from "react";
import { Button, FloatingLabel, Form } from "react-bootstrap";
import { connect } from "react-redux";
import { useHistory } from "react-router-dom";
import { toast } from "react-toastify";
import { getCreateProjectRequest } from "../../store/Queries";
import { Project } from "../../store/redux-query";
import Modal from "../Layout/Utils/Modal";

interface CreateProjectFormProps {
  addProject: (project: Project) => any;
  closeModalFunc: () => void;
}

function CreateProjectForm(props: CreateProjectFormProps) {
  const prjNameInputRef = useRef<HTMLInputElement>(null);
  const prjDecriptionInputRef = useRef<HTMLTextAreaElement>(null);
  const history = useHistory();

  function createPrjBtnHandler(event: FormEvent) {
    event.preventDefault();
    const prjName = prjNameInputRef.current!.value;
    const prjDescription = prjDecriptionInputRef.current!.value;
    const prj = {
      id: prjName.replace(" ", "_"),
      name: prjName,
      description: prjDescription,
    };
    props.addProject(prj).then((result: any) => {
      if (result.status !== 201) {
        toast.error("Nie udało się utworzyć projektu!");
        props.closeModalFunc();
      } else {
        props.closeModalFunc();
        history.push(`/edit/${prj.id}`, { projectID: prj.id });
      }
    });
  }

  return (
    <Modal text="" inputFlag={true}>
      <Form onSubmit={createPrjBtnHandler}>
        <Form.Group className="mb-3">
          <Form.Label>Nazwa:</Form.Label>
          <Form.Control
            type="text"
            required
            maxLength={30}
            ref={prjNameInputRef}
          />
          <Form.Text className="text-muted">
            Maksymalna liczba znaków dla nazwy projektu: 30
          </Form.Text>
        </Form.Group>
        <Form.Group>
          <FloatingLabel label="Opis projektu">
            <Form.Control
              as="textarea"
              placeholder="Leave a comment here"
              style={{ height: "100px" }}
              ref={prjDecriptionInputRef}
            />
          </FloatingLabel>
        </Form.Group>
        <Button variant="primary" type="submit">
          Zatwierdź
        </Button>
      </Form>
    </Modal>
  );
}

const mapStateToProps = (state: any) => {
  return {};
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    addProject: (project: Project) => {
      return dispatch(getCreateProjectRequest(project));
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(CreateProjectForm);
