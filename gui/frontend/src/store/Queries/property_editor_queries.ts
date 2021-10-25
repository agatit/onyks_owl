import { mutateAsync, requestAsync } from "redux-query";
import {
  listModuleParams,
  ListModuleParamsRequest,
  listQueueParams,
  ListQueueParamsRequest,
  ModuleParam,
  QueueParam,
  TypedQueryConfig,
  updateModule,
  updateModuleParam,
  UpdateModuleParamRequest,
  UpdateModuleRequest,
  updateQueue,
  updateQueueParam,
  UpdateQueueParamRequest,
  UpdateQueueRequest,
} from "../redux-query";

export const getModuleParamsRequest = (
  requestParams: ListModuleParamsRequest,
  config?: TypedQueryConfig<
    { moduleParams: Array<ModuleParam> },
    Array<ModuleParam>
  >
) => {
  return requestAsync(listModuleParams(requestParams, config));
};

export const getUpdateModuleParamRequest = (
  requestParams: UpdateModuleParamRequest
) => {
  return mutateAsync(updateModuleParam(requestParams));
};

export const getUpdateModuleRequest = (requestParams: UpdateModuleRequest) => {
  return mutateAsync(updateModule(requestParams));
};

//   project({projectId})/module({moduleId})/param

export const getQueueParamsRequest = (
  requestParams: ListQueueParamsRequest,
  config?: TypedQueryConfig<
    { queueParams: Array<QueueParam> },
    Array<QueueParam>
  >
) => {
  return requestAsync(listQueueParams(requestParams, config));
};

export const getUpdateQueueParamRequest = (
  requestParams: UpdateQueueParamRequest
) => {
  return mutateAsync(updateQueueParam(requestParams));
};

export const getUpdateQueueRequest = (requestParams: UpdateQueueRequest) => {
  return mutateAsync(updateQueue(requestParams));
};
