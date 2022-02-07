import { OwlNodeModel } from "../../Components/OwlNodes/OwlNodeModel";
import { OwlQueueModel } from "../../Components/OwlQueue/OwlQueueModel";
import { nodesListActionTypes } from "../Reducers/nodesListReducer";

export const addNode = (node: OwlNodeModel | OwlQueueModel) => ({
  type: nodesListActionTypes.ADD_NODE,
  node,
});

export const deleteNode = (node: OwlNodeModel | OwlQueueModel) => ({
  type: nodesListActionTypes.DELETE_NODE,
  node,
});
