import { NodeModel } from "../../Components/CustomDiagramNodes/NodeModel";

export const nodeActionTypes = {
  SET_SELECTED_NODE: "SET_SELECTED_NODE",
};

const initialState = {
  selectedNode: {},
  test: true,
};

interface nodeAction {
  type: string;
  node: NodeModel;
}

export const nodesData = (state = initialState, action: nodeAction) => {
  switch (action.type) {
    case nodeActionTypes.SET_SELECTED_NODE:
      return { ...state, selectedNode: action.node, test: !state.test };
    default:
      return state;
  }
};
