import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams";
import { OwlNodeModel } from "./Components/OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "./Components/OwlQueue/OwlQueueModel";
import { OwlQueueLinkModel } from "./Components/OwlQueueLinks/OwlQueueLinkModel";
import { BASE_PATH } from "./store/redux-query";

export async function loadQueues(engine: DiagramEngine, projectId: string) {
  const queuesUrl = BASE_PATH + `/project(${projectId})/queue`;
  const url = "../project(Test)/queue.json"; //url testowe
  const resp = await fetch(queuesUrl);
  const queuesFromResponse = await resp.json();

  for (let i in queuesFromResponse) {
    var newQueue = new OwlQueueModel(queuesFromResponse[i]);
    engine.getModel().addNode(newQueue);
  }
  engine.repaintCanvas();
  loadNodes(engine, projectId);
}

export async function loadNodes(engine: DiagramEngine, projectId: string) {
  const nodesUrl = BASE_PATH + `/project(${projectId})/module`;

  const url = "../project(Test)/module.json"; //url testowe
  const resp = await fetch(nodesUrl);
  const data = await resp.json();

  const nodesArray: OwlNodeModel[] = [];

  for (let i in data) {
    var newNode = new OwlNodeModel(data[i]);
    console.log(newNode);
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
        // Do ewentualnej zmiany z racji hardcode,
        //  ale nie jest to istotne w obecnej implementacji kolejek
      );
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
        // Do ewentualnej zmiany z racji hardcode,
        //  ale nie jest to istotne w obecnej implementacji kolejek
      );
      engine.getModel().addLink(link);
    }
  }
  engine.repaintCanvas();
}

export function loadSchema(engine: DiagramEngine, projectId: string) {
  engine.setModel(new DiagramModel());
  loadQueues(engine, projectId);
}
