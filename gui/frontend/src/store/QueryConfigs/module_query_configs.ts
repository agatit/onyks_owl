import { Module, TypedQueryConfig } from "../redux-query";

export const ModuleListRequestConfig: TypedQueryConfig<
  { modules: Array<Module> },
  Array<Module>
> = {
  transform: (response: Array<Module>) => {
    return {
      modules: response,
    };
  },
  update: {
    modules: (prevVal, newVal) => newVal,
  },
  force: true,
};
