import { useRef } from "react";
import { Form } from "react-bootstrap";
import { connect, useSelector } from "react-redux";
import { useRequest } from "redux-query-react";
import {
  getProjectRequest,
  getUpdateProjectRequest,
} from "../../../../store/Queries";
import { ProjectRequestConfig } from "../../../../store/QueryConfigs";
import { getProject, Project } from "../../../../store/redux-query";
import { selectProject } from "../../../../store/selectors/projectSelectors";
import { maxProjectNameLength } from "../../CreateProjectForm";
import TabSection from "../../Tabs/TabSection";

interface ProjectEditorProps {
  projectId: string;
  getProjectParams: (projectId: string, config?: any) => void;
  updateProject: (project: Project) => void;
}

function ProjectEditor(props: ProjectEditorProps) {
  const [{ isPending, status }, refresh] = useRequest(
    getProject({ projectId: props.projectId }, ProjectRequestConfig)
  );

  const descriptionTextAreaRef = useRef<HTMLTextAreaElement>(null);
  const prjNameInputRef = useRef<HTMLInputElement>(null);

  const descriptionInputBlurHandler = (project: Project) => {
    if (descriptionTextAreaRef.current != null) {
      const currentDesc = descriptionTextAreaRef.current.value;
      project.description = currentDesc;
      props.updateProject(project);
    }
  };

  const project: Project = useSelector(selectProject);

  // if (typeof status === "number" && status >= 400) {
  //   return <div>"Coś poszło nie tak! Spróbuj ponownie!"</div>;
  // }

  const propertyInputBlurHandler = (newValue: string) => {
    project.name = newValue;
    props.updateProject(project);
  };

  // if (isPending || !project) {
  //   return <div>Trwa ładowanie...</div>;
  // }

  return (
    <TabSection title="Główne">
      <Form.Group className="mb-3">
        <Form.Label style={propLabels}>Nazwa</Form.Label>
        <Form.Control
          type="text"
          required
          onBlur={(e) => {
            propertyInputBlurHandler(e.target.value);
          }}
          maxLength={30}
          ref={prjNameInputRef}
          style={propInputs}
          defaultValue={props.projectId}
        />
        <Form.Text className="text-muted">
          Maksymalna liczba znaków dla nazwy projektu: {maxProjectNameLength}
        </Form.Text>
      </Form.Group>
      {/* <textarea
        rows={6}
        defaultValue={project.description ? project.description : ""}
        ref={descriptionTextAreaRef}
        onBlur={() =>
          descriptionInputBlurHandler({
            id: project.id,
            name: project.name,
            description: project.description,
          })
        }
        style={propInputs}
      ></textarea> */}
    </TabSection>
  );
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    getProjectParams: (projectId: string, config?: any) => {
      dispatch(getProjectRequest(projectId, config));
    },
    updateProject: (project: Project) => {
      dispatch(getUpdateProjectRequest(project));
    },
  };
};

export default connect(undefined, mapDispatchToProps)(ProjectEditor);

const propInputs = {
  backgroundColor: "rgb(143, 143, 143)",
  border: "none",
  padding: "10px",
  marginRight: "20px",
  fontFamily: "Arial",
  color: "rgb(220, 220, 220)",
  borderTopLeftRadius: "0.25rem",
  borderBottomLeftRadius: "0.25rem",
  width: "80%",
  margin: "auto",
};

const propLabels = {
  width: "35%",
  padding: "0.375rem 0.75rem",
  backgroundColor: "inherit",
  color: "rgb(180, 180, 180)",
  border: "none",
};
