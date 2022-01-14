import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { DiagramEngine } from "@projectstorm/react-diagrams";
import { connect } from "react-redux";
import { OwlQueueModel } from "../../OwlQueue/OwlQueueModel";

interface AddNodeFormProps {
  engine: DiagramEngine;
}

function AddNodeForm(props: AddNodeFormProps) {
  function AddQueueToSchema() {
    let newNode = new OwlQueueModel({});
    props.engine.getModel().addNode(newNode);
    props.engine.repaintCanvas();
  }

  return (
    <div>
      <h2>Dodaj kolejkę</h2>
      <FontAwesomeIcon
        icon={faPlus}
        size="3x"
        onClick={AddQueueToSchema}
        color="gray"
      />
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return { engine: state.engineReducer.engine, test: state.nodesData.test };
};

export default connect(mapStateToProps)(AddNodeForm);
