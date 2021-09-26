import React from "react";
import classses from "./Toolbar.module.css";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";
import { NodeModel } from "../CustomDiagramNodes/NodeModel";
import { connect } from "react-redux";
import { store } from "../../store/store";
import { useRef } from "react";
import { selectedNode } from "../../store/Actions/nodeActions";
import { TextInput } from "../UI/Inputs";

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

  if (node === undefined) {
    return (
      <div className={classses.toolBar}>
        <h2>Brak wybranego modułu</h2>
      </div>
    );
  }

  return (
    <div className={classses.toolBar}>
      <h2>{node.title ? node.title : "Brak nazwy modułu"}</h2>
      <TextInput
        ref={nameInputRef}
        onChangeAction={handlePropertyChange}
        id="name-input"
        initValue={node.title}
        labelText="Nazwa: "
        propName={titleProp}
        refNum={10}
      />

      {props.node.params !== undefined &&
        Object.keys(props.node.params).map((paramKey, index) => {
          return (
            <TextInput
              ref={addToRefs}
              onChangeAction={handlePropertyChange}
              id={node.params[paramKey] + "-" + node.module_id}
              initValue={node.params[paramKey]}
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
