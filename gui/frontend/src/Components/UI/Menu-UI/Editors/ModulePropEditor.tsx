import { FormControl, InputGroup } from "react-bootstrap";
import {
  ModuleParam,
  UpdateModuleParamRequest,
  UpdateModuleRequest,
} from "../../../../store/redux-query";
import { OwlNodeModel } from "../../../OwlNodes/OwlNodeModel";
import { useEffect } from "react";
import { selectedNode } from "../../../../store/Actions/nodeActions";
import store from "../../../../store/store";
import {
  getModuleParamsRequest,
  getUpdateModuleParamRequest,
  getUpdateModuleRequest,
} from "../../../../store/Queries/property_editor_queries";
import { ModuleParamListConfig } from "../../../../store/QueryConfigs/property_query_configs";
import { connect, useSelector } from "react-redux";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";

import classes from "./ModulePropEditor.module.css";
import { selectModuleParams } from "../../../../store/selectors/propertySelectors";

interface ModulePropEditorProps {
  node: OwlNodeModel;
  engine: DiagramEngine;
  projectId: string;
  getModuleParams: (projectId: string, moduleId: string) => void;
  updateParamRequest: (requestParams: UpdateModuleParamRequest) => void;
  updateModule: (requestParams: UpdateModuleRequest) => void;
}

function ModulePropEditor(props: ModulePropEditorProps) {
  const engine = props.engine;
  const node = props.node;

  useEffect(() => {
    if (node) props.getModuleParams(props.projectId, node.id);
  }, [node]);

  // DO POPRAWY
  const handleNamePropertyChange = (newValue: string) => {
    node.title = newValue;
    store.dispatch(selectedNode(node));
    engine.repaintCanvas();
  };

  const moduleNameInputBlurHandler = (newValue: string) => {
    node.name = newValue;
    props.updateModule({ projectId: props.projectId, module: node });
  };

  const handlePropertyChange = (newValue: string, param: ModuleParam) => {
    param.value = newValue;
    store.dispatch(selectedNode(node));
    engine.repaintCanvas();
  };

  const propertyInputBlurHandler = (newValue: string, param: ModuleParam) => {
    param.value = newValue;
    props.updateParamRequest({
      projectId: props.projectId,
      moduleId: node.id,
      moduleParam: param,
    });
  };

  const propertyList: Array<ModuleParam> = useSelector(selectModuleParams);

  return (
    <div className={classes.toolBar}>
      <h2>{node.title ? node.title : "Brak nazwy modułu"}</h2>
      <InputGroup className="mb-3">
        <InputGroup.Text id="inputGroup-sizing-default">Nazwa</InputGroup.Text>
        <FormControl
          value={node.title}
          aria-label="Default"
          aria-describedby="inputGroup-sizing-default"
          onChange={(e) => handleNamePropertyChange(e.target.value)}
          onBlur={(e) => moduleNameInputBlurHandler(e.target.value)}
        />
      </InputGroup>

      {propertyList !== undefined &&
        propertyList.map((paramKey: ModuleParam, index: number) => {
          return (
            <InputGroup className="mb-3" key={index}>
              <InputGroup.Text id="inputGroup-sizing-default">
                {paramKey.paramDefId}
              </InputGroup.Text>
              <FormControl
                value={paramKey.value}
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                onChange={(e) => handlePropertyChange(e.target.value, paramKey)}
                onBlur={(e) =>
                  propertyInputBlurHandler(e.target.value, paramKey)
                }
              />
            </InputGroup>
          );
        })}
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    test: state.nodesData.test,
    engine: state.engineReducer.engine,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    getModuleParams: (projectId: string, moduleId: string) => {
      dispatch(
        getModuleParamsRequest(
          { projectId: projectId, moduleId: moduleId },
          ModuleParamListConfig
        )
      );
    },
    updateParamRequest: (requestParams: UpdateModuleParamRequest) => {
      dispatch(getUpdateModuleParamRequest(requestParams));
    },
    updateModule: (requestParams: UpdateModuleRequest) => {
      dispatch(getUpdateModuleRequest(requestParams));
    },
  };
};

const connector = connect(
  mapStateToProps,
  mapDispatchToProps
)(ModulePropEditor);

export default connector;
