import { DiagramEngine } from "@projectstorm/react-diagrams";
import { Button } from "react-bootstrap";
import { connect } from "react-redux";
import { addNode } from "../../../store/Actions/nodeListActions";
import store from "../../../store/store";
import { OwlQueueModel } from "../../OwlQueue/OwlQueueModel";
import TabSection from "../Tabs/TabSection";

interface AddNodeFormProps {
  engine: DiagramEngine;
}

function AddNodeForm(props: AddNodeFormProps) {
  function AddQueueToSchema() {
    let newNode = new OwlQueueModel({});
    props.engine.getModel().addNode(newNode);
    store.dispatch(addNode(newNode));
    props.engine.repaintCanvas();
  }

  return (
    <TabSection title="Nowa kolejka">
      <h4 style={{ color: "wheat" }}>Przeciągnij, aby dodać</h4>
      <Button
        draggable={true}
        variant="dark"
        onDragStart={(event) => {
          event.dataTransfer.setData("diagram-queue", "");
        }}
      >
        Kolejka
      </Button>
    </TabSection>
  );
}

const mapStateToProps = (state: any) => {
  return { engine: state.engineReducer.engine, test: state.nodesData.test };
};

export default connect(mapStateToProps)(AddNodeForm);
