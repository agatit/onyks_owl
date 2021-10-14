import { faEdit, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Project } from "../../../store/redux-query/models/Project";
import { useHistory } from "react-router-dom";

interface ProjectListProps {
  projects: Project[];
}

function ProjectList(props: ProjectListProps) {
  const history = useHistory();

  const editBtnHandler = () => {
    history.push("/edit");
  };

  const wrapListElement = (project: Project) => {
    const path = "/player/";
    return (
      <ListGroup.Item as="li">
        <Link to={path} style={{ textDecoration: "none" }}>
          <Button variant="dark">{project.id}</Button>
        </Link>
        <Link to="/edit" style={{ textDecoration: "none" }}>
          <FontAwesomeIcon icon={faEdit} size="lg" />
        </Link>
        <FontAwesomeIcon icon={faTrashAlt} size="lg" onClick={editBtnHandler} />
      </ListGroup.Item>
    );
  };

  return (
    <ListGroup as="ul">
      {props.projects &&
        props.projects.map((project) => wrapListElement(project))}
    </ListGroup>
  );
}

export default ProjectList;
