import { QueryConfig } from "redux-query";
import {
  Configuration,
  Module,
  ModuleDef,
  TypedQueryConfig,
} from "../redux-query";

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

export const ModuleListDefsRequestConfig: QueryConfig = {
  url: `${Configuration.basePath}/module_def`,
  transform: (response: Array<ModuleDef>) => {
    return {
      modules_defs: response,
    };
  },
  update: {
    modules_defs: (prevVal, newVal) => newVal,
  },
  force: true,
};
