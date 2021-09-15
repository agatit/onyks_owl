import { DefaultLinkModel, DiagramModel } from "@projectstorm/react-diagrams";
import { NodeFactory } from "./Components/CustomDiagramNodes/NodeFactory";
import { NodeModel } from "./Components/CustomDiagramNodes/NodeModel";
import { CanvasWidget } from "@projectstorm/react-canvas-core";
import { CustomLinkFactory } from "./Components/CustomLinks/CustomLinkFactory";
import { CustomLinkModel } from "./Components/CustomLinks/CustomLinkModel";

export const Diagrams = (props: any) => {
  // create an instance of the engine with all the defaults

  function onNodeDrop(event: React.DragEvent<HTMLDivElement>) {
    var moduleData = JSON.parse(event.dataTransfer.getData("diagram-node"));
    const droppedNode = new NodeModel({
      color: "LemonChiffon",
      title: moduleData.name,
      content: "Source",
      source: true,
    });
    droppedNode.setPosition(engine.getRelativeMousePoint(event));
    engine.getModel().addNode(droppedNode);

    engine.repaintCanvas();
  }

  const engine = props.engine;
  engine.getNodeFactories().registerFactory(new NodeFactory());
  engine.getLinkFactories().registerFactory(new CustomLinkFactory());
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
    color: "LightCyan",
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
  // --- node function
  const node5 = new NodeModel({
    color: "Lavender",
    title: "Moduł",
    inputs: ["Dane", "Dane 2"],
    outputs: ["Wyj", "Wyj 2"],
  });
  node5.setPosition(650, 100);
  // --- node outputs
  const node6 = new NodeModel({
    color: "LightCyan",
    title: "Dane wyjściowe",
    content: "Data",
  });
  node6.setPosition(900, 100);

  // TESTOWY SCHEMAT
  const linkBase = new CustomLinkModel();
  linkBase.setSourcePort(node1.getPort("Out"));
  linkBase.setTargetPort(node3.getPort("In"));
  const linkTest = engine.getFactoryForLink(linkBase).generateModel({});
  const link1 = new CustomLinkModel();
  link1.setSourcePort(node1.getPort("Out"));
  link1.setTargetPort(node3.getPort("In"));
  const link3 = new DefaultLinkModel();
  link3.setSourcePort(node2.getPort("Out"));
  link3.setTargetPort(node5.getPort("Dane"));
  const link4 = new DefaultLinkModel();
  link4.setSourcePort(node3.getPort("Out"));
  link4.setTargetPort(node5.getPort("Dane 2"));
  const link5 = new DefaultLinkModel();
  link5.setSourcePort(node5.getPort("Wyj"));
  link5.setTargetPort(node6.getPort("In"));

  const model = new DiagramModel();
  model.addAll(node1, node2, node3, node5, node6, link1, link3, link4, link5);

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
