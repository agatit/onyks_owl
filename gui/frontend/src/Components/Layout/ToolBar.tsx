import classses from "./Toolbar.module.css";
import { connect, useSelector } from "react-redux";
import { OwlNodeModel } from "../OwlNodes/OwlNodeModel";

import { isQueueSelected } from "../../store/selectors/queueSelectors";
import ModulePropEditor from "../UI/Menu-UI/Editors/ModulePropEditor";
import QueuePropEdtior from "../UI/Menu-UI/Editors/QueuePropEdtior";

// REFERENCJE CHYBA DO WYWALENIA!!!!!!!!!!!!!

interface toolBarProps {
  node: OwlNodeModel;
  projectId: string;
}

function ToolBar(props: toolBarProps) {
  const node = props.node;

  //const nameInputRef = useRef<HTMLInputElement>(null);
  //const refArray = useRef<any>([]);

  //refArray.current = [];

  /*
  const addToRefs = (el: HTMLInputElement) => {
    if (el && !refArray.current.includes(el)) {
      refArray.current.push(el);
    }
  };
*/

  const queueSelected: boolean = useSelector(isQueueSelected);

  if (node === undefined) {
    return (
      <div className={classses.toolBar}>
        <h2>Brak wybranego modułu</h2>
      </div>
    );
  }

  {
    if (queueSelected) {
      return <QueuePropEdtior projectId={props.projectId} />;
    }
  }

  return <ModulePropEditor projectId={props.projectId} />;
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    test: state.nodesData.test,
  };
};

const connector = connect(mapStateToProps)(ToolBar);

export default connector;
