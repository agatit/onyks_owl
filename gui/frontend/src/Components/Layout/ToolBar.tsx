import React, { useEffect, useState } from "react";
import data from "../../data/schemas/testSchema3.json";
import classses from "./Toolbar.module.css";
import Button from "../UI/Button";
import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams-core";
import getNotification, { NotificationType } from "../UI/Notification";
import { NodeModel } from "../CustomDiagramNodes/NodeModel";
import { connect } from "react-redux";
import { store } from "../../store/store";
import { useRef } from "react";
import { selectedNode } from "../../store/Actions/nodeActions";
import { TextInput } from "../UI/Inputs";
import { parseClassName } from "react-toastify/dist/utils";

interface toolBarProps {
  engine: DiagramEngine;
  node: NodeModel;
}

function ToolBar(props: toolBarProps) {
  const engine = props.engine;
  const node = props.node;
  const titleProp = "Title";

  const nameInputRef = useRef<HTMLInputElement>(null);
  const refArray = useRef<any>([]);

  refArray.current = [];

  const handlePropertyChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    propertyName: string,
    refNum: number
  ) => {
    if (propertyName === titleProp) {
      node.title = nameInputRef.current!.value;
    } else {
      node.params[propertyName] = refArray.current[refNum].value;
      node.content = node.params[propertyName];
    }
    store.dispatch(selectedNode(node));
    engine.repaintCanvas();
  };

  const addToRefs = (el: HTMLInputElement) => {
    if (el && !refArray.current.includes(el)) {
      refArray.current.push(el);
    }
  };

  return (
    <div className={classses.toolBar}>
      <h2>
        Moduł: {props.node.title ? props.node.title : "Brak wybranego modułu"}
      </h2>
      <TextInput
        ref={nameInputRef}
        onChangeAction={handlePropertyChange}
        id="name-input"
        initValue={props.node.title}
        labelText="Nazwa: "
        propName={titleProp}
        refNum={10}
      />

      {props.node.params != undefined &&
        Object.keys(props.node.params).map((paramKey, index) => {
          return (
            <TextInput
              ref={addToRefs}
              onChangeAction={handlePropertyChange}
              id={props.node.params[paramKey] + "-" + props.node.module_id}
              initValue={props.node.params[paramKey]}
              labelText={
                paramKey.charAt(0).toUpperCase() + paramKey.slice(1) + ": "
              }
              propName={paramKey}
              refNum={index}
            />
          );
        })}
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return { node: state.nodesData.selectedNode, test: state.nodesData.test };
};

const connector = connect(mapStateToProps)(ToolBar);

export default connector;
