import { FormControl, InputGroup } from "react-bootstrap";
import {
  QueueParam,
  UpdateQueueParamRequest,
  UpdateQueueRequest,
} from "../../../../store/redux-query";
import store from "../../../../store/store";
import {
  getUpdateQueueParamRequest,
  getUpdateQueueRequest,
} from "../../../../store/Queries/property_editor_queries";
import { connect, useSelector } from "react-redux";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";
import { selectQueueParams } from "../../../../store/selectors/propertySelectors";
import { selectedQueue } from "../../../../store/Actions/queueActions";
import classes from "./QueuePropEditor.module.css";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { OwlNodeModel } from "../../../OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "../../../OwlQueue/OwlQueueModel";
import TabSection from "../../Tabs/TabSection";

interface QueuePropEditorProps {
  queue: OwlQueueModel;
  engine: DiagramEngine;
  projectId: string;
  node: OwlNodeModel;
  updateParamRequest: (requestParams: UpdateQueueParamRequest) => void;
  updateQueue: (requestParams: UpdateQueueRequest) => void;
}

function QueuePropEditor(props: QueuePropEditorProps) {
  const engine = props.engine;
  const queue = props.queue;

  // DO POPRAWY
  const handleNamePropertyChange = (newValue: string) => {
    queue.name = newValue;
    store.dispatch(selectedQueue(queue));
    engine.repaintCanvas();
  };

  const moduleNameInputBlurHandler = (newValue: string) => {
    queue.name = newValue;
    props.updateQueue({ projectId: props.projectId, queue: queue });
  };

  const handlePropertyChange = (newValue: string, param: QueueParam) => {
    param.value = newValue;
    store.dispatch(selectedQueue(queue));
    engine.repaintCanvas();
  };

  const propertyInputBlurHandler = (newValue: string, param: QueueParam) => {
    param.value = newValue;
    props.updateParamRequest({
      projectId: props.projectId,
      queueId: queue.id,
      queueParam: param,
    });
  };

  const propertyList: Array<QueueParam> = useSelector(selectQueueParams);

  if (!queue) {
    return (
      <div>
        <h2 className={classes.warning}>Brak wybranej kolejki</h2>

        <FontAwesomeIcon
          icon={faTimes}
          size="5x"
          color="gray"
        ></FontAwesomeIcon>
      </div>
    );
  }
  if (props.node) props.node.setSelected(false);
  queue.setSelected(true);

  return (
    <TabSection title="Główne">
      <InputGroup className="mb-3">
        <InputGroup.Text id="inputGroup-sizing-default" style={propLabels}>
          Nazwa
        </InputGroup.Text>
        <FormControl
          value={queue.name}
          onChange={(e) => handleNamePropertyChange(e.target.value)}
          onBlur={(e) => moduleNameInputBlurHandler(e.target.value)}
          style={propInputs}
        />
      </InputGroup>

      {propertyList !== undefined &&
        propertyList.map((paramKey: QueueParam, index: number) => {
          return (
            <InputGroup className="mb-3" key={index}>
              <InputGroup.Text
                id="inputGroup-sizing-default"
                style={propLabels}
              >
                {paramKey.paramsDefId}
              </InputGroup.Text>
              <FormControl
                value={paramKey.value}
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                onChange={(e) => handlePropertyChange(e.target.value, paramKey)}
                onBlur={(e) =>
                  propertyInputBlurHandler(e.target.value, paramKey)
                }
                style={propInputs}
              />
            </InputGroup>
          );
        })}
    </TabSection>
  );
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    queue: state.queueReducer.selectedQueue,
    test: state.queueReducer.test,
    engine: state.engineReducer.engine,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    updateParamRequest: (requestParams: UpdateQueueParamRequest) => {
      dispatch(getUpdateQueueParamRequest(requestParams));
    },
    updateQueue: (requestParams: UpdateQueueRequest) => {
      dispatch(getUpdateQueueRequest(requestParams));
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(QueuePropEditor);

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
