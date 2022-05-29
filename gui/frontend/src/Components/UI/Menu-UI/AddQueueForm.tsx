import { DiagramEngine } from "@projectstorm/react-diagrams";
import { Button } from "react-bootstrap";
import { connect } from "react-redux";
import TabSection from "../Tabs/TabSection";

interface AddQueueFormProps {
  engine: DiagramEngine;
}

export const queueTransferName = "diagram-queue";

function AddQueueForm(props: AddQueueFormProps) {
  return (
    <TabSection title="Nowa kolejka">
      <h4 style={{ color: "wheat" }}>Przeciągnij, aby dodać</h4>
      <Button
        draggable={true}
        variant="dark"
        onDragStart={(event) => {
          event.dataTransfer.setData(queueTransferName, "");
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

export default connect(mapStateToProps)(AddQueueForm);
