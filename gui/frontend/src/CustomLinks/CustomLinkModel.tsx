import { DefaultLinkModel } from "@projectstorm/react-diagrams";

export class CustomLinkModel extends DefaultLinkModel {
  constructor() {
    super({
      type: "test",
      width: 10,
    });
  }
}
