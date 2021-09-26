import { NodeModel } from "../../Components/CustomDiagramNodes/NodeModel";
import { nodeActionTypes } from "../Reducers/nodeReducer";

export const selectedNode = (node: NodeModel) => ({
  type: nodeActionTypes.SET_SELECTED_NODE,
  node,
});

export const deleteNode = (node: NodeModel) => ({
  type: nodeActionTypes.ON_NODE_DELETE,
  node,
});
