import { combineReducers } from "redux";
import { nodesData } from "./nodeReducer";
import { engineReducer } from "./engineReducer";

export default combineReducers({
  nodesData,
  engineReducer,
});
