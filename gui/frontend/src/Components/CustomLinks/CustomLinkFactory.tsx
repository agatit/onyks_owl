import { DefaultLinkFactory } from "@projectstorm/react-diagrams";
import { CustomLinkModel } from "./CustomLinkModel";

export class CustomLinkFactory extends DefaultLinkFactory {
  constructor() {
    super("test");
  }

  generateModel() {
    console.log("Custom link created - CustomLinkFactory");
    return new CustomLinkModel();
  }
}