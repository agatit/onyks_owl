import { OwlNodeModel } from "../../Components/OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "../../Components/OwlQueue/OwlQueueModel";
import { nodeActionTypes } from "../Reducers/nodeReducer";

export const selectedNode = (node: OwlNodeModel) => ({
  type: nodeActionTypes.SET_SELECTED_NODE,
  node,
});

export const deleteNode = (node: OwlNodeModel) => ({
  type: nodeActionTypes.ON_NODE_DELETE,
  node,
});
