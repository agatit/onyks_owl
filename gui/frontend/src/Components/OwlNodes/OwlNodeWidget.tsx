import * as React from "react";
import clsx from "clsx";
import { DiagramEngine, PortWidget } from "@projectstorm/react-diagrams-core";
import { OwlNodeModel } from "./OwlNodeModel";
import store from "../../store/store";
import { deleteNode, selectedNode } from "../../store/Actions/nodeActions";
import { getDeleteModuleFromProjectRequest } from "../../store/Queries/project_editor_queries";
import styled from "@emotion/styled";
import { ModuleParam } from "../../store/redux-query";

import classes from "./OwlNodeWidget.module.css";

export interface NodeWidgetProps {
  node: OwlNodeModel;
  engine: DiagramEngine;
}

export interface NodeWidgetState {}

class OwlNodeAbstractWidget extends React.Component<
  NodeWidgetProps,
  NodeWidgetState
> {
  constructor(props: NodeWidgetProps) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div
        className={clsx("custom-node-content")}
        style={{ backgroundColor: this.props.node.bodyColor }}
      >
        {!this.props.node.source && (
          <PortWidget
            engine={this.props.engine}
            port={this.props.node.inputPortModel}
            className={clsx("circle-porter", "circle-porter-in")}
          >
            <div className={clsx("circle-port")} />
          </PortWidget>
        )}
        <OwlNodeContent node={this.props.node} engine={this.props.engine} />
        <PortWidget
          engine={this.props.engine}
          port={this.props.node.outputPortModel}
          className={clsx("circle-porter", "circle-porter-out")}
        >
          <div className={clsx("circle-port")} />
        </PortWidget>
      </div>
    );
  }
}

interface OwlNodeContentProps extends NodeWidgetProps {
  node: OwlNodeModel;
}

const OwlNodeContent = (props: OwlNodeContentProps) => {
  const WrapParameterListElement = (parameter: ModuleParam, index: number) => {
    return (
      <div className={classes.parameter} key={index}>
        <div className={classes.paramterName}>{parameter.paramDefId}</div>
        <div className={classes.parameterValue}>{parameter.value}</div>
      </div>
    );
  };

  return (
    <div className={classes.parametersList}>
      {props.node.parameters.map((param, index) =>
        WrapParameterListElement(param, index)
      )}
      <div className={classes.description}>{props.node.description}</div>
    </div>
  );
};

export class OwlNodeWidget extends React.Component<NodeWidgetProps> {
  constructor(props: NodeWidgetProps) {
    super(props);
    this.state = {};
    this.props.node.registerListener({
      entityRemoved: ({ entity }: any) => {
        store.dispatch(deleteNode(this.props.node));
        store.dispatch(
          getDeleteModuleFromProjectRequest(
            this.props.node.project.id,
            this.props.node.id
          )
        );
      },
    });
  }
  handleClick = () => {
    store.dispatch(selectedNode(this.props.node));
  };

  render() {
    return (
      <div className="custom-node" onClick={this.handleClick}>
        <StyledNodeWidget selected={this.props.node.isSelected()}>
          <div
            className="custom-node-header"
            style={{ backgroundColor: this.props.node.headerColor }}
          >
            {this.props.node.name}
          </div>
          <OwlNodeAbstractWidget
            node={this.props.node}
            engine={this.props.engine}
          />
        </StyledNodeWidget>
      </div>
    );
  }
}

const StyledNodeWidget = styled.div<{ selected: boolean }>`
  ${(p) => p.selected && `border: 3px solid rgb(4, 189, 209);`}
`;
