import { NodeWidget } from "@projectstorm/react-diagrams-core";
import { NodeModel } from "../../Components/CustomDiagramNodes/NodeModel";
import { nodeActionTypes } from "../Reducers/nodeReducer";

export const selectedNode = (node: NodeModel) => ({
  type: nodeActionTypes.SET_SELECTED_NODE,
  node,
});
