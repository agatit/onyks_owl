import { Form, FormControl, InputGroup } from "react-bootstrap";

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
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { OwlQueueLinkModel } from "../../../OwlQueueLinks/OwlQueueLinkModel";

interface ModulePropEditorProps {
  queue: OwlQueueLinkModel;
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
    //if (node) props.getModuleParams(props.projectId, node.id);
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
  if (props.queue) props.queue.setSelected(false);
  node.setSelected(true);

  return (
    <div>
      <div className={classes.propertiesBars}>
        <div className={classes.propsTitle}>Główne</div>
        <InputGroup className="mb-3">
          <InputGroup.Text id="inputGroup-sizing-default" style={propLabels}>
            Nazwa
          </InputGroup.Text>
          <FormControl
            value={node.title}
            aria-label="Default"
            aria-describedby="inputGroup-sizing-default"
            onChange={(e) => handleNamePropertyChange(e.target.value)}
            onBlur={(e) => moduleNameInputBlurHandler(e.target.value)}
            style={propInputs}
          />
        </InputGroup>

        {propertyList !== undefined &&
          propertyList.map((paramKey: ModuleParam, index: number) => {
            return (
              <InputGroup className="mb-3" key={index}>
                <InputGroup.Text
                  id="inputGroup-sizing-default"
                  style={propLabels}
                >
                  {paramKey.paramDefId}
                </InputGroup.Text>
                <FormControl
                  style={propInputs}
                  value={paramKey.value}
                  aria-label="Default"
                  aria-describedby="inputGroup-sizing-default"
                  onChange={(e) =>
                    handlePropertyChange(e.target.value, paramKey)
                  }
                  onBlur={(e) =>
                    propertyInputBlurHandler(e.target.value, paramKey)
                  }
                />
              </InputGroup>
            );
          })}
      </div>
      <LookPropsEditor node={node} engine={engine} />
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return {
    queue: state.queueReducer.selectedQueue,
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

export const LookPropsEditor = (props: {
  node: OwlNodeModel;
  engine: DiagramEngine;
}) => {
  const colorInputChangeHandler = (color: string) => {
    props.node.color = color;
    store.dispatch(selectedNode(props.node));
  };

  return (
    <div className={[classes.propertiesBars, classes.lookBars].join(" ")}>
      <div className={classes.propsTitle}>Wygląd</div>
      <Form.Label htmlFor="colorPicker" style={propLabels}>
        Kolor nagłówka
      </Form.Label>
      <Form.Control
        style={colorPickerStyle}
        type="color"
        id="colorPicker"
        value={props.node.color}
        onChange={(e) => colorInputChangeHandler(e.target.value)}
        title="Wybierz kolor"
      ></Form.Control>
      <Form.Label htmlFor="colorPicker" style={propLabels}>
        Kolor modułu
      </Form.Label>
      <Form.Control
        style={colorPickerStyle}
        type="color"
        id="colorPicker"
        defaultValue="#563d7c"
        title="Wybierz kolor"
      ></Form.Control>
    </div>
  );
};

// style css

const propInputs = {
  backgroundColor: "rgb(143, 143, 143)",
  border: "none",
  padding: "10px",
  marginRight: "20px",
  fontFamily: "Arial",
  color: "rgb(220, 220, 220)",
  borderTopLeftRadius: "0.25rem",
  borderBottomLeftRadius: "0.25rem",
};

const propLabels = {
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
