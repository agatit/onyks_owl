import { DiagramEngine } from "@projectstorm/react-diagrams";
import { AddNodeBtn } from "./Buttons/NodeGenerator";
import React from "react";

export interface MenuProps {
  engine: DiagramEngine;
}

export class Menu extends React.Component<MenuProps> {
  constructor(public props: any) {
    super(props);
  }

  render() {
    return (
      <div>
        <AddNodeBtn engine={this.props.engine} />
        <button type="submit" className="add-button">
          test
        </button>
      </div>
    );
  }
}
