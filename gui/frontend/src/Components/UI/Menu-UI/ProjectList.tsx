import { faEdit, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, ListGroup } from "react-bootstrap";
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
import { useEffect, useRef, useState } from "react";
import { ProjectListRequestConfig } from "../../../store/QueryConfigs";
import Backdrop from "../../Layout/Utils/Backdrop";
import store from "../../../store/store";

interface ProjectListProps {
  projects: Array<Project>;
  deleteProject: (projectID: string) => any;
  getProjectList: () => void;
  updateProject: (project: Project) => void;
}

function ProjectList(props: ProjectListProps) {
  const history = useHistory();

  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      props.getProjectList();
      setIsPending(false);
    }, 4000);
  }, []);

  const editBtnHandler = (projectId: string) => {
    history.push(`/edit/${projectId}`, { projectID: projectId });
  };

  const deleteBtnHandler = (projectId: string, projectIndex: number) => {
    props.deleteProject(projectId).then((result: any) => {
      if (result.status !== 200) {
        console.log("Nie udało się usunąć projetku!");
      } else {
        console.log("Projekt usunięty pomyślnie!");
      }
    });
  };

  const projectBtnHandler = (projectId: string) => {
    history.push(`/player/${projectId}`, { projectID: projectId });
  };

  const wrapListElement = (project: Project, index: number) => {
    const path = "/player/";
    return (
      <ListGroup.Item
        as="li"
        id={classes.visible}
        key={index}
        bsPrefix={classes.test}
      >
        <div
          className={classes.prjTitle}
          onClick={() => {
            projectBtnHandler(project.id);
          }}
        >
          {project.name}
        </div>
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
        {/*
        {project.description && (
          <textarea
            id={classes.hidden}
            rows={3}
            defaultValue={project.description}
            ref={descriptionTextAreaRef}
            onBlur={() =>
              descriptionInputBlurHandler({
                id: project.id,
                name: project.name,
                description: project.description,
              })
            }
          ></textarea>
          */}
      </ListGroup.Item>
    );
  };

  if (isPending) {
    return <Backdrop />;
  }

  return (
    <ListGroup as="ul">
      {props.projects &&
        props.projects.map((project, index) => wrapListElement(project, index))}
    </ListGroup>
  );
}

const mapStateToProps = (state: any) => {
  return {
    projects: selectProjectList(state),
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    getProjectList: () => {
      dispatch(getProjectListRequest(ProjectListRequestConfig));
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
