import {
  DefaultLabelFactory,
  DiagramEngine,
  DiagramModel,
} from "@projectstorm/react-diagrams";
import { NodeFactory } from "./Components/CustomDiagramNodes/NodeFactory";
import { NodeModel } from "./Components/CustomDiagramNodes/NodeModel";
import {
  CanvasWidget,
  DeleteItemsAction,
} from "@projectstorm/react-canvas-core";
import { DemoCanvasWidget } from "./Components/Layout/CanvasWidget";
import { useEffect, useState } from "react";
import Modal from "./Components/Layout/Utils/Modal";
import Backdrop from "./Components/Layout/Utils/Backdrop";
import { connect } from "react-redux";

const Diagrams = (props: any) => {
  function onNodeDrop(event: React.DragEvent<HTMLDivElement>) {
    var moduleData = JSON.parse(event.dataTransfer.getData("diagram-node"));
    // const moduleProps = Object.keys(moduleData);
    const droppedNode = new NodeModel({
      color: "LemonChiffon",
      title: moduleData.name,
      content: "Source",
    });
    droppedNode.params = moduleData["params"];
    droppedNode.module_id = moduleData["id"];

    droppedNode.setPosition(engine.getRelativeMousePoint(event));
    engine.getModel().addNode(droppedNode);

    engine.repaintCanvas();
  }

  async function loadSchema() {
    const url = "testSchema3.json";
    const resp = await fetch(url);
    const data = await resp.json();

    var newModel = new DiagramModel();
    var modelString = JSON.stringify(data);
    newModel.deserializeModel(JSON.parse(modelString), engine);
    engine.setModel(newModel);
    setSchemaLoading(false);
  }

  const engine = props.engine;
  const [isSchemaLoading, setSchemaLoading] = useState(true);
  engine.getNodeFactories().registerFactory(new NodeFactory());
  engine.getLabelFactories().registerFactory(new DefaultLabelFactory());

  engine
    .getActionEventBus()
    .registerAction(new DeleteItemsAction({ keyCodes: [46] }));

  useEffect(() => {
    console.log("ładowanie");

    setTimeout(loadSchema, 4000);
  }, []);

  if (isSchemaLoading) {
    engine.setModel(new DiagramModel());
    return (
      <div
        className="App"
        onDrop={(event) => {
          onNodeDrop(event);
        }}
        onDragOver={(event) => {
          event.preventDefault();
        }}
      >
        <DemoCanvasWidget>
          <CanvasWidget className="diagram-container" engine={engine} />
        </DemoCanvasWidget>
        ;{isSchemaLoading && <Modal text="Trwa ładowanie schematu..." />}
        {isSchemaLoading && <Backdrop />}
      </div>
    );
  }

  return (
    <div
      className="App"
      onDrop={(event) => {
        onNodeDrop(event);
      }}
      onDragOver={(event) => {
        event.preventDefault();
      }}
    >
      <DemoCanvasWidget>
        <CanvasWidget className="diagram-container" engine={engine} />
      </DemoCanvasWidget>
    </div>
  );
};

const mapStateToProps = (state: any) => {
  return { engine: state.engineReducer.engine, test: state.nodesData.test };
};

const connector = connect(mapStateToProps)(Diagrams);

export default connector;
