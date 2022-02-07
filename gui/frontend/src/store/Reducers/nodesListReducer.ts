import { OwlNodeModel } from "../../Components/OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "../../Components/OwlQueue/OwlQueueModel";

export const nodesListActionTypes = {
  ADD_NODE: "ADD_NODE",
  DELETE_NODE: "DELETE_NODE",
};

const initialState = {
  schemaElements: Array<OwlNodeModel | OwlQueueModel>(),
};

interface nodeAction {
  type: string;
  node: OwlNodeModel | OwlQueueModel;
}

export const nodesList = (state = initialState, action: nodeAction) => {
  switch (action.type) {
    case nodesListActionTypes.ADD_NODE:
      state.schemaElements.push(action.node);
      return {
        ...state,
      };
    case nodesListActionTypes.DELETE_NODE:
      return {
        ...state,
        schemaElements: state.schemaElements.slice(
          state.schemaElements.indexOf(action.node),
          1
        ),
      };
    default:
      return state;
  }
};
