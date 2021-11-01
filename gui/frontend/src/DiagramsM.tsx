import {
  DefaultLabelFactory,
  DiagramEngine,
  DiagramModel,
} from "@projectstorm/react-diagrams";
import {
  CanvasWidget,
  DeleteItemsAction,
} from "@projectstorm/react-canvas-core";
import { DemoCanvasWidget } from "./Components/Layout/CanvasWidget";
import { useEffect, useRef, useState } from "react";
import Modal from "./Components/Layout/Utils/Modal";
import Backdrop from "./Components/Layout/Utils/Backdrop";
import { connect } from "react-redux";
import {
  getCreateModuleRequest,
  getDeleteModuleFromProjectRequest,
} from "./store/Queries/project_editor_queries";
import { Module } from "./store/redux-query";
import { OwlNodeModel } from "./Components/OwlNodes/OwlNodeModel";
import { OwlNodeFactory } from "./Components/OwlNodes/OwlNodeFactory";
import { OwlQueueLinkFactory } from "./Components/OwlQueueLinks/OwlQueueLinkFactory";
import { useLocation } from "react-router";
import html2canvas from "html2canvas";
import { EditableLabelFactory } from "./Components/CustomLinks/Labels/LabelFactory";

interface DiagramProps {
  engine: DiagramEngine;
  addModuleRequest: (projectId: string, module: Module) => void;
  projectId: string;
  deleteNodeRequest: (projectId: string, moduleId: string) => void;
}

const Diagrams = (props: DiagramProps) => {
  function onNodeDrop(event: React.DragEvent<HTMLDivElement>) {
    var moduleData = JSON.parse(event.dataTransfer.getData("diagram-node"));
    // const moduleProps = Object.keys(moduleData);
    const droppedNode = new OwlNodeModel({
      ...moduleData,
      color: "LemonChiffon",
      title: moduleData.name,
      content: "Opis",
    });
    droppedNode.params = moduleData["params"];
    droppedNode.module_id = moduleData["id"];
    console.log(droppedNode.id);
    droppedNode.setPosition(engine.getRelativeMousePoint(event));
    engine.getModel().addNode(droppedNode);
    props.addModuleRequest(props.projectId, droppedNode);
    engine.repaintCanvas();
  }

  const location = useLocation();
  const canvaRef = useRef(null);

  useEffect(() => {
    console.log(canvaRef.current);
    html2canvas(canvaRef.current!).then((canvas) =>
      document.body.appendChild(canvas)
    );
  }, [location]);

  /*
  async function loadSchema() {
    const url = "../testSchema3.json";
    const resp = await fetch(url);
    const data = await resp.json();

    var newModel = new DiagramModel();
    var modelString = JSON.stringify(data);
    newModel.deserializeModel(JSON.parse(modelString), engine);
    engine.setModel(newModel);
    setSchemaLoading(false);
  }
*/
  const engine = props.engine;
  const [isSchemaLoading, setSchemaLoading] = useState(true);
  engine.getNodeFactories().registerFactory(new OwlNodeFactory());
  engine.getLabelFactories().registerFactory(new EditableLabelFactory());
  engine.getLinkFactories().registerFactory(new OwlQueueLinkFactory());

  engine
    .getActionEventBus()
    .registerAction(new DeleteItemsAction({ keyCodes: [46] }));

  useEffect(() => {
    setTimeout(() => {
      setSchemaLoading(false);
    }, 4000);
  }, []);

  if (isSchemaLoading) {
    engine.setModel(new DiagramModel());
    return (
      <div className="App">
        <DemoCanvasWidget>
          <CanvasWidget className="diagram-container" engine={engine} />
        </DemoCanvasWidget>
        <Modal text="Trwa ładowanie schematu..." />
        <Backdrop />
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
      id="userCanva"
      ref={canvaRef}
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

const mapDispatchToProps = (dispatch: any) => {
  return {
    addModuleRequest: (projectId: string, module: Module) => {
      dispatch(getCreateModuleRequest(projectId, module));
    },
    deleteNodeRequest: (projectId: string, moduleId: string) => {
      dispatch(getDeleteModuleFromProjectRequest(projectId, moduleId));
    },
  };
};

const connector = connect(mapStateToProps, mapDispatchToProps)(Diagrams);

export default connector;
