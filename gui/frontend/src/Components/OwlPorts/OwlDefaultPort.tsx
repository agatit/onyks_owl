import { DefaultPortModel } from "@projectstorm/react-diagrams";
import { OwlQueueLinkModel } from "../OwlQueueLinks/OwlQueueLinkModel";

export class OwlDefaultPort extends DefaultPortModel {
  createLinkModel(): OwlQueueLinkModel {
    return new OwlQueueLinkModel();
  }

  canLinkToPort(port: OwlDefaultPort) {
    if (this.options.in === port.getOptions().in) return false;
    const thisLinks = Object.values(this.getLinks());
    const targetPortLinks = Object.values(port.getLinks());
    if (thisLinks.length > 1 || targetPortLinks.length > 0) return false;
    return true;
  }
}
