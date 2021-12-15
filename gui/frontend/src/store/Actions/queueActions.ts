import { OwlQueueModel } from "../../Components/OwlQueue/OwlQueueModel";
import { OwlQueueLinkModel } from "../../Components/OwlQueueLinks/OwlQueueLinkModel";
import { queueActionTypes } from "../Reducers/queueReducer";

export const selectedQueue = (queue: OwlQueueModel) => ({
  type: queueActionTypes.SET_SELECTED_QUEUE,
  queue,
});

export const deleteQueue = (queue: OwlQueueModel) => ({
  type: queueActionTypes.ON_QUEUE_DELETE,
  queue,
});
