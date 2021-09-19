import { NodeModel } from "../../Components/CustomDiagramNodes/NodeModel";

export const nodeActionTypes = {
  SET_SELECTED_NODE: "SET_SELECTED_NODE",
};

const initialState = {
  selectedNode: {},
  test: "s",
};

interface nodeAction {
  type: string;
  node: NodeModel;
}

export const nodesData = (state = initialState, action: nodeAction) => {
  switch (action.type) {
    case nodeActionTypes.SET_SELECTED_NODE:
      console.log(
        "In reducer! - " + action.node.title + " test: " + state.test
      );
      return { ...state, selectedNode: action.node, test: state.test + "1" };
    default:
      return state;
  }
};
