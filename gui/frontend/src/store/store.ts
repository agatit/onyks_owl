import { applyMiddleware, createStore, combineReducers } from "redux";
import { entitiesReducer, queriesReducer, queryMiddleware } from "redux-query";
import superagentInterface from "redux-query-interface-superagent";
import { nodesData } from "./Reducers/nodeReducer";
import { engineReducer } from "./Reducers/engineReducer";
import { queueReducer } from "./Reducers/queueReducer";
import { nodesList } from "./Reducers/nodesListReducer";

export const getQueries = (state: any) => state.queries;
export const getEntities = (state: any) => state.entities;

const reducer = combineReducers({
  nodesData,
  engineReducer,
  queueReducer,
  nodesList,
  entities: entitiesReducer,
  queries: queriesReducer,
});

const store = createStore(
  reducer,
  applyMiddleware(queryMiddleware(superagentInterface, getQueries, getEntities))
);

export default store;
