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
import { OwlQueueLinkModel } from "../../../OwlQueueLinks/OwlQueueLinkModel";
import { selectedQueue } from "../../../../store/Actions/queueActions";

import classes from "./QueuePropEditor.module.css";

interface QueuePropEditorProps {
  queue: OwlQueueLinkModel;
  engine: DiagramEngine;
  projectId: string;
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

  return (
    <div className={classes.toolBar}>
      <h2>{queue.name ? queue.name : "Brak nazwy kolejki"}</h2>
      <InputGroup className="mb-3">
        <InputGroup.Text id="inputGroup-sizing-default">Nazwa</InputGroup.Text>
        <FormControl
          value={queue.name}
          aria-label="Default"
          aria-describedby="inputGroup-sizing-default"
          onChange={(e) => handleNamePropertyChange(e.target.value)}
          onBlur={(e) => moduleNameInputBlurHandler(e.target.value)}
        />
      </InputGroup>

      {propertyList !== undefined &&
        propertyList.map((paramKey: QueueParam, index: number) => {
          return (
            <InputGroup className="mb-3" key={index}>
              <InputGroup.Text id="inputGroup-sizing-default">
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
              />
            </InputGroup>
          );
        })}
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return {
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
