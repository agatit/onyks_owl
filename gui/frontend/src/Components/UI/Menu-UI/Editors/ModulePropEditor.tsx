import { Form, FormControl, InputGroup } from "react-bootstrap";
import {
  ModuleParam,
  ModuleParamFromJSON,
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
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import TabSection from "../../Tabs/TabSection";
import { repaintCanvas } from "../../../../store/Actions/engineActions";

interface ModulePropEditorProps {
  node: OwlNodeModel;
  engine: DiagramEngine;
  projectId: string;
  getModuleParams: (
    projectId: string,
    moduleId: string,
    node: OwlNodeModel
  ) => void;
  updateParamRequest: (requestParams: UpdateModuleParamRequest) => void;
  updateModule: (requestParams: UpdateModuleRequest) => void;
}

function ModulePropEditor(props: ModulePropEditorProps) {
  const engine = props.engine;
  const node = props.node;

  useEffect(() => {
    var prjId = props.projectId[0].toUpperCase() + props.projectId.slice(1);
    if (node) props.getModuleParams(prjId, node.id, node);
  }, [node]);

  const handleNamePropertyChange = (newValue: string) => {
    node.name = newValue;
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

  if (!node) {
    return (
      <div>
        <h2 className={classes.warning}>Brak wybranego modułu</h2>
        <FontAwesomeIcon
          icon={faTimes}
          size="5x"
          color="gray"
        ></FontAwesomeIcon>
      </div>
    );
  }

  return (
    <TabSection title="Główne">
      <InputGroup className="mb-3">
        <InputGroup.Text id="inputGroup-sizing-default" style={propLabelsStyle}>
          Nazwa
        </InputGroup.Text>
        <FormControl
          style={propInputsStyle}
          value={node.name}
          aria-label="Default"
          aria-describedby="inputGroup-sizing-default"
          onChange={(e) => handleNamePropertyChange(e.target.value)}
          onBlur={(e) => moduleNameInputBlurHandler(e.target.value)}
        />
      </InputGroup>

      {node.parameters.length !== 0 &&
        node.parameters.map((paramKey: ModuleParam, index: number) => {
          return (
            <InputGroup className="mb-3" key={index}>
              <InputGroup.Text
                id="inputGroup-sizing-default"
                style={propLabelsStyle}
              >
                {paramKey.paramDefId}
              </InputGroup.Text>
              <FormControl
                style={propInputsStyle}
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
      <LookPropsEditor node={node} engine={engine} />
    </TabSection>
  );
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    test: state.nodesData.test,
    engine: state.engineReducer.engine,
  };
};

export const LookPropsEditor = (props: {
  node: OwlNodeModel;
  engine: DiagramEngine;
}) => {
  const headerColorChangeHandler = (color: string) => {
    props.node.headerColor = color;
    store.dispatch(repaintCanvas());
  };

  const bodyColorChangeHandler = (color: string) => {
    props.node.bodyColor = color;
    store.dispatch(repaintCanvas());
  };

  return (
    <TabSection title="Wygląd">
      <Form.Label htmlFor="colorPicker" style={propLabelsStyle}>
        Kolor nagłówka
      </Form.Label>
      <Form.Control
        style={colorPickerStyle}
        type="color"
        id="colorPicker"
        defaultValue={props.node.headerColor}
        onChange={(e) => headerColorChangeHandler(e.target.value)}
        title="Wybierz kolor"
      ></Form.Control>
      <Form.Label htmlFor="colorPicker" style={propLabelsStyle}>
        Kolor modułu
      </Form.Label>
      <Form.Control
        style={colorPickerStyle}
        type="color"
        id="colorPicker"
        defaultValue={props.node.bodyColor}
        onChange={(e) => bodyColorChangeHandler(e.target.value)}
        title="Wybierz kolor"
      ></Form.Control>
    </TabSection>
  );
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    getModuleParams: (
      projectId: string,
      moduleId: string,
      node: OwlNodeModel
    ) => {
      dispatch(
        getModuleParamsRequest(
          { projectId: projectId, moduleId: moduleId },
          ModuleParamListConfig
        )
      ).then((result: any) => {
        node.parameters = result.body.map(ModuleParamFromJSON);
        store.dispatch(selectedNode(node));
      });
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

// style css

const propInputsStyle = {
  backgroundColor: "rgb(143, 143, 143)",
  border: "none",
  padding: "10px",
  marginRight: "20px",
  fontFamily: "Arial",
  color: "rgb(220, 220, 220)",
  borderTopLeftRadius: "0.25rem",
  borderBottomLeftRadius: "0.25rem",
};

const propLabelsStyle = {
  width: "35%",
  padding: "0.375rem 0.75rem",
  backgroundColor: "inherit",
  color: "rgb(180, 180, 180)",
  border: "none",
  paddingLeft: "1rem",
  marginLeft: "auto",
};

const colorPickerStyle = {
  display: "inline-block",
};
