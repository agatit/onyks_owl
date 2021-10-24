export const isQueueSelected = (state: any) => {
  if (state.queueReducer.selectedQueue) return true;
  else return false;
};
