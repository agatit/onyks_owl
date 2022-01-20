import { NodeModel } from "@projectstorm/react-diagrams";
import { ListGroup } from "react-bootstrap";
import { OwlNodeModel } from "../../OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "../../OwlQueue/OwlQueueModel";
import TabSection from "../Tabs/TabSection";

interface ProjectMenageListProps {
  schemaElements: Array<any>;
}

function ProjectMenageList(props: ProjectMenageListProps) {
  function elementClickHandler(element: NodeModel) {
    element.setSelected(true);
  }

  function wrapListElement(listElement: OwlNodeModel | OwlQueueModel) {
    return (
      <ListGroup.Item
        style={propInputs}
        onClick={() => {
          elementClickHandler(listElement);
        }}
      >
        {listElement.name}
      </ListGroup.Item>
    );
  }

  return (
    <TabSection title="Lista obiektów">
      <ListGroup as="ul">
        {props.schemaElements.map((element, index) => {
          return wrapListElement(element);
        })}
      </ListGroup>
    </TabSection>
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
