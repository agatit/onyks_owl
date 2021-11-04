import { OwlNodeModel } from "../../Components/OwlNodes/OwlNodeModel";

export const nodeActionTypes = {
  SET_SELECTED_NODE: "SET_SELECTED_NODE",
  ON_NODE_DELETE: "ON_NODE_DELETE",
};

const initialState = {
  selectedNode: undefined,
  test: true,
};

interface nodeAction {
  type: string;
  node: OwlNodeModel;
}

export const nodesData = (state = initialState, action: nodeAction) => {
  switch (action.type) {
    case nodeActionTypes.SET_SELECTED_NODE:
      return { ...state, selectedNode: action.node, test: !state.test };
    case nodeActionTypes.ON_NODE_DELETE:
      return { ...state, selectedNode: undefined, test: !state.test };
    default:
      return state;
  }
};
