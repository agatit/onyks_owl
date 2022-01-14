import { DefaultNodeModel, NodeModel } from "@projectstorm/react-diagrams";
import { ListGroup } from "react-bootstrap";

import classes from "./Editors/ModulePropEditor.module.css";

interface schemaElement {
  title: string;
  id: any;
}

interface ProjectMenageListProps {
  schemaElements: Array<NodeModel>;
}

function ProjectMenageList(props: ProjectMenageListProps) {
  function elementClickHandler(element: NodeModel) {
    element.setSelected(true);
  }

  function wrapListElement(listElement: NodeModel) {
    return (
      <ListGroup.Item
        style={propInputs}
        onClick={() => {
          elementClickHandler(listElement);
        }}
      ></ListGroup.Item>
    );
  }

  return (
    <div className={classes.propertiesBars}>
      <div className={classes.propsTitle}>Lista obiektów</div>
      <ListGroup as="ul">
        {props.schemaElements.map((element, index) => {
          return wrapListElement(element);
        })}
      </ListGroup>
    </div>
  );
}

export default ProjectMenageList;

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
  marginTop: "5px",
  cursor: "pointer",
};
