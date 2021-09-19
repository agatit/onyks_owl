import {
  DefaultLinkModel,
  DiagramEngine,
  DiagramModel,
} from "@projectstorm/react-diagrams";
import { NodeFactory } from "./Components/CustomDiagramNodes/NodeFactory";
import { NodeModel } from "./Components/CustomDiagramNodes/NodeModel";
import { CanvasWidget } from "@projectstorm/react-canvas-core";
import { CustomLinkFactory } from "./Components/CustomLinks/CustomLinkFactory";
import { CustomLinkModel } from "./Components/CustomLinks/CustomLinkModel";

interface diagramProps {
  engine: DiagramEngine;
}

export const Diagrams = (props: diagramProps) => {
  // create an instance of the engine with all the defaults

  function onNodeDrop(event: React.DragEvent<HTMLDivElement>) {
    var moduleData = JSON.parse(event.dataTransfer.getData("diagram-node"));
    const droppedNode = new NodeModel({
      color: "LemonChiffon",
      title: moduleData.name,
      content: "Source",
    });
    droppedNode.setPosition(engine.getRelativeMousePoint(event));
    engine.getModel().addNode(droppedNode);

    engine.repaintCanvas();
  }

  const engine = props.engine;
  engine.getNodeFactories().registerFactory(new NodeFactory());

  // --- node source
  const node1 = new NodeModel({
    color: "LemonChiffon",
    title: "Źródło OUT",
    content: "Source",
    source: true,
  });
  node1.setPosition(100, 100);
  // --- node data
  const node2 = new NodeModel({
    color: "LemonChiffon",
    title: "Źródło IN/OUT",
    content: "Dane",
  });
  node2.setPosition(350, 100);
  const node3 = new NodeModel({
    color: "LightCyan",
    title: "Źródło IN/OUT",
    content: "Dane",
  });
  node3.setPosition(350, 200);

  // TESTOWY SCHEMAT
  const link1 = new DefaultLinkModel();
  link1.setSourcePort(node1.getPort("Out"));
  link1.setTargetPort(node3.getPort("In"));

  const model = new DiagramModel();
  model.addAll(node1, node2, node3, link1);

  engine.setModel(model);
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
      <CanvasWidget className="diagram-container" engine={engine} />
    </div>
  );
};

// TODO: Odczyt schematów z API
