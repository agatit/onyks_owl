import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams";
import { CanvasWidget } from "@projectstorm/react-canvas-core";
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
import { useLocation } from "react-router";
import { loadSchema } from "./DiagramTools";

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
      color: "#ffB730",
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
    //console.log(canvaRef.current);
    loadSchema(engine);
    // html2canvas(canvaRef.current!).then((canvas) =>
    //   document.body.appendChild(canvas)
    // );
  }, [location]);

  const engine = props.engine;
  const [isSchemaLoading, setSchemaLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setSchemaLoading(false);
    }, 1000);
  }, []);

  if (isSchemaLoading) {
    const testModel = new DiagramModel();
    engine.setModel(testModel);
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
