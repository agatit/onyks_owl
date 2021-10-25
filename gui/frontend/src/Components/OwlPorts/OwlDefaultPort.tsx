import { DefaultPortModel } from "@projectstorm/react-diagrams";
import { OwlNodeModel } from "../OwlNodes/OwlNodeModel";
import { OwlQueueLinkModel } from "../OwlQueueLinks/OwlQueueLinkModel";

export class OwlDefaultPort extends DefaultPortModel {
  createLinkModel(): OwlQueueLinkModel {
    return new OwlQueueLinkModel();
  }
}
