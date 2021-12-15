import { DefaultLinkFactory } from "@projectstorm/react-diagrams";
import { OwlQueueLinkModel } from "./OwlQueueLinkModel";

export class OwlQueueLinkFactory extends DefaultLinkFactory {
  constructor() {
    super("OwlQueueLink");
  }

  generateModel() {
    return new OwlQueueLinkModel();
  }
}
