import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams";
import { CanvasWidget } from "@projectstorm/react-canvas-core";
import { DemoCanvasWidget } from "./Components/Layout/CanvasWidget";
import { useEffect, useRef, useState } from "react";
import Modal from "./Components/Layout/Utils/Modal";
import Backdrop from "./Components/Layout/Utils/Backdrop";
import { connect, useDispatch } from "react-redux";
import {
  getCreateModuleRequest,
  getCreateQueueRequest,
  getDeleteModuleFromProjectRequest,
} from "./store/Queries/project_editor_queries";
import { Module, Project, Queue } from "./store/redux-query";
import { OwlNodeModel } from "./Components/OwlNodes/OwlNodeModel";
import { useLocation } from "react-router";
import { OwlQueueModel } from "./Components/OwlQueue/OwlQueueModel";
import { addNode } from "./store/Actions/nodeListActions";
import { toast } from "react-toastify";
import { loadSchema } from "./DiagramTools";

interface DiagramProps {
  engine: DiagramEngine;
  addModuleRequest: (projectId: string, module: Module) => any;
  addQueueRequest: (projectId: string, queue: Queue) => any;
  projectInfo?: Project;
  projectId: string;
  deleteNodeRequest: (projectId: string, moduleId: string) => void;
}

const Diagrams = (props: DiagramProps) => {
  const dispatch = useDispatch();

  const canvaRef = useRef(null);
  const engine = props.engine;
  const [isSchemaLoading, setSchemaLoading] = useState(true);

  function onNodeDrop(event: React.DragEvent<HTMLDivElement>) {
    var droppedNode: OwlNodeModel | OwlQueueModel;
    if (event.dataTransfer.types[0] === "diagram-node") {
      var moduleData = JSON.parse(event.dataTransfer.getData("diagram-node"));
      droppedNode = new OwlNodeModel({
        ...moduleData,
        project: props.projectInfo,
      });
      console.log(props.projectInfo);

      props
        .addModuleRequest(props.projectId, droppedNode)
        .then((result: any) => {
          if (result.status !== 200) {
            toast.error("Nie udało się dodać modułu!");
          } else {
            droppedNode.setPosition(engine.getRelativeMousePoint(event));
            dispatch(addNode(droppedNode));
            engine.getModel().addNode(droppedNode);
            engine.repaintCanvas();
          }
        });
    } else {
      droppedNode = new OwlQueueModel({ project: props.projectInfo });
      props
        .addQueueRequest(props.projectId, droppedNode)
        .then((result: any) => {
          if (result.status !== 200) {
            toast.error("Nie udało się dodać kolejki!");
          } else {
            // Po implementacji zwrotu Id w metodzie POST przez serwer - przypisać tutaj id z odpowiedzi
            droppedNode.setPosition(engine.getRelativeMousePoint(event));
            dispatch(addNode(droppedNode));
            engine.getModel().addNode(droppedNode);
            engine.repaintCanvas();
          }
        });
    }
  }

  useEffect(() => {
    loadSchema(engine, props.projectId);
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
      return dispatch(getCreateModuleRequest(projectId, module));
    },
    addQueueRequest: (projectId: string, queue: Queue) => {
      return dispatch(
        getCreateQueueRequest({ projectId: projectId, queue: queue })
      );
    },
    deleteNodeRequest: (projectId: string, moduleId: string) => {
      dispatch(getDeleteModuleFromProjectRequest(projectId, moduleId));
    },
  };
};

const connector = connect(mapStateToProps, mapDispatchToProps)(Diagrams);

export default connector;
