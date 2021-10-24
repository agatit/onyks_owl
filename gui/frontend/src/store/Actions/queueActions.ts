import { OwlQueueLinkModel } from "../../Components/OwlQueueLinks/OwlQueueLinkModel";
import { queueActionTypes } from "../Reducers/queueReducer";

export const selectedQueue = (queue: OwlQueueLinkModel) => ({
  type: queueActionTypes.SET_SELECTED_QUEUE,
  queue,
});

export const deleteQueue = (queue: OwlQueueLinkModel) => ({
  type: queueActionTypes.ON_QUEUE_DELETE,
  queue,
});
