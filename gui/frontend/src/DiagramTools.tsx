import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams";
import { OwlNodeModel } from "./Components/OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "./Components/OwlQueue/OwlQueueModel";
import { OwlQueueLinkModel } from "./Components/OwlQueueLinks/OwlQueueLinkModel";
import { BASE_PATH } from "./store/redux-query";

export async function loadQueues(engine: DiagramEngine, projectId: string) {
  const url = BASE_PATH + `/project(${projectId})/queue`;
  //const url = "../project(Test)/queue.json";
  const resp = await fetch(url);
  const data = await resp.json();

  for (let i in data) {
    var newQueue = new OwlQueueModel(data[i]);
    engine.getModel().addNode(newQueue);
  }
  engine.repaintCanvas();
  loadNodes(engine, projectId);
}

export async function loadNodes(engine: DiagramEngine, projectId: string) {
  const url = BASE_PATH + `/project(${projectId})/module`;
  //const url = "../project(Test)/module.json";
  const resp = await fetch(url);
  const data = await resp.json();

  const nodesArray: OwlNodeModel[] = [];

  for (let i in data) {
    var newNode = new OwlNodeModel(data[i]);
    nodesArray.push(newNode);
    engine.getModel().addNode(newNode);
  }
  engine.repaintCanvas();
  generateLinks(nodesArray, engine);
}

// do ulepszenia - zmiana na bardziej uniwersalne i zmiana sposobu sprawdzania !!!

export function generateLinks(nodesArr: OwlNodeModel[], engine: DiagramEngine) {
  for (let i = 0; i < nodesArr.length; i++) {
    if (
      nodesArr[i].input &&
      engine.getModel().getNode(nodesArr[i].input.id) !== undefined
    ) {
      const link = new OwlQueueLinkModel();

      link.setSourcePort(nodesArr[i].inputPortModel);
      link.setTargetPort(
        engine.getModel().getNode(nodesArr[i].input.id).getPort("Wyjście")
      );
      // console.log(link);
      engine.getModel().addLink(link);
    }
    if (
      nodesArr[i].output &&
      engine.getModel().getNode(nodesArr[i].output.id) !== undefined
    ) {
      const link = new OwlQueueLinkModel();
      link.setSourcePort(nodesArr[i].outputPortModel);
      link.setTargetPort(
        engine.getModel().getNode(nodesArr[i].output.id).getPort("Wejście")
      );
      //console.log(link);
      engine.getModel().addLink(link);
    }
  }
  engine.repaintCanvas();
}

export function loadSchema(engine: DiagramEngine, projectId: string) {
  engine.setModel(new DiagramModel());
  loadQueues(engine, projectId);
}
