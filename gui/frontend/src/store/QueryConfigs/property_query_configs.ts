import { ModuleParam, QueueParam, TypedQueryConfig } from "../redux-query";

export const ModuleParamListConfig: TypedQueryConfig<
  { moduleParams: Array<ModuleParam> },
  Array<ModuleParam>
> = {
  transform: (response: Array<ModuleParam>) => {
    return {
      moduleParams: response,
    };
  },
  update: {
    moduleParams: (prevVal, newVal) => newVal,
  },
  force: true,
};

export const QueueParamListConfig: TypedQueryConfig<
  { queueParams: Array<QueueParam> },
  Array<QueueParam>
> = {
  transform: (response: Array<QueueParam>) => {
    return {
      queueParams: response,
    };
  },
  update: {
    queueParams: (prevVal, newVal) => newVal,
  },
  force: true,
};
