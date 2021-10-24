import { DefaultLinkModel } from "@projectstorm/react-diagrams";

export class CustomLinkModel extends DefaultLinkModel {
  constructor() {
    super({
      type: "OwlQueue",
      width: 10,
    });
  }
}
