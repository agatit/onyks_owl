import { faEdit, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  Container,
  ListGroup,
  Spinner,
  Col,
  Row,
  Stack,
  Card,
} from "react-bootstrap";
import { Project } from "../../../store/redux-query/models/Project";
import { useHistory } from "react-router-dom";
import {
  getDeleteProjectRequest,
  getProjectListRequest,
  getUpdateProjectRequest,
} from "../../../store/Queries";
import classes from "./ProjectList.module.css";
import { selectProjectList } from "../../../store/selectors/projectSelectors";
import { connect } from "react-redux";
import { ProjectListRequestConfig } from "../../../store/QueryConfigs";
import Backdrop from "../../Layout/Utils/Backdrop";
import { useRequest } from "redux-query-react";
import { toast, ToastContainer } from "react-toastify";
import { useRef } from "react";

interface ProjectListProps {
  projects: Array<Project>;
  deleteProject: (projectID: string) => any;
  getProjectList: () => any;
  updateProject: (project: Project) => void;
}

function ProjectList(props: ProjectListProps) {
  const history = useHistory();

  const [{ isPending, status }, refresh] = useRequest(ProjectListRequestConfig);

  if (isPending) {
    return (
      <Container fluid>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <h4>Trwa ładowanie projektów!</h4>
      </Container>
    );
  }

  if (typeof status === "number" && (status >= 400 || status < 200)) {
    toast.error("Brak połączenia z serwerem!");
    return <h6>Brak połączenia, spróbuj odświeżyć stronę!</h6>;
  }

  const editBtnHandler = (projectId: string) => {
    history.push(`/edit/${projectId}`, { projectID: projectId });
  };

  const deleteBtnHandler = (projectId: string, projectIndex: number) => {
    props.deleteProject(projectId).then((result: any) => {
      if (result.status !== 200) {
        toast.error("Nie udało się usunąć projetku!");
      } else {
        toast.success("Projekt usunięty pomyślnie!");
        refresh();
      }
    });
  };

  const projectBtnHandler = (projectId: string) => {
    history.push(`/player/${projectId}`, { projectID: projectId });
  };

  const createColumn = (colElement: Project, index: number) => {
    return <Col>{createTableElement(colElement, index)}</Col>;
  };

  const createRow = (rowElements: Array<Project>) => {
    return (
      <Row sm={3} md={3} xs={3} lg={3}>
        {rowElements &&
          rowElements.map((project, index) => {
            return createColumn(project, index);
          })}
      </Row>
    );
  };

  const createProjectTable = (projects: Array<Project>) => {
    return (
      <Container fluid className="h-100">
        {createRow(projects)}
      </Container>
    );
  };

  const createTableElement = (project: Project, index: number) => {
    return (
      <Card>
        <Card.Header
          onClick={() => {
            projectBtnHandler(project.id);
          }}
        >
          {project.name}
        </Card.Header>
        <Card.Body>
          <Card.Text>
            {project.description ? project.description : "Brak opisu projektu"}
          </Card.Text>
          <FontAwesomeIcon
            icon={faEdit}
            size="lg"
            className={classes.list_util}
            onClick={() => {
              editBtnHandler(project.id);
            }}
          />
          <FontAwesomeIcon
            icon={faTrashAlt}
            size="lg"
            onClick={() => {
              deleteBtnHandler(project.id, index);
            }}
            className={classes.list_util}
          />
        </Card.Body>
      </Card>
    );
  };

  if (isPending) {
    return <Backdrop />;
  }
  if (typeof status === "number" && status >= 400) {
    return <div>Coś poszło nie tak! Spróbuj odświeżyć stronę!</div>;
  }
  if (!props.projects) {
    return <div>Brak utworzonych projektów</div>;
  }

  return createProjectTable(props.projects);
}

const mapStateToProps = (state: any) => {
  return {
    projects: selectProjectList(state),
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    getProjectList: (): number => {
      return dispatch(getProjectListRequest(ProjectListRequestConfig));
    },
    updateProject: (project: Project) => {
      dispatch(getUpdateProjectRequest(project));
    },
    deleteProject: (projectID: string): number => {
      return dispatch(getDeleteProjectRequest(projectID));
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectList);
