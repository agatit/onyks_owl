import { OwlQueueLinkModel } from "../../Components/OwlQueueLinks/OwlQueueLinkModel";

export const queueActionTypes = {
  SET_SELECTED_QUEUE: "SET_SELECTED_QUEUE",
  ON_QUEUE_DELETE: "ON_QUEUE_DELETE",
};

const initialState = {
  selectedQueue: undefined,
  test: true,
};

interface queueAction {
  type: string;
  queue: OwlQueueLinkModel;
}

export const queueReducer = (state = initialState, action: queueAction) => {
  switch (action.type) {
    case queueActionTypes.SET_SELECTED_QUEUE:
      return { ...state, selectedQueue: action.queue, test: !state.test };
    case queueActionTypes.ON_QUEUE_DELETE:
      return { ...state, selectedQueue: undefined, test: !state.test };
    default:
      return state;
  }
};
