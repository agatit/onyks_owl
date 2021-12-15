import { mutateAsync, requestAsync } from "redux-query";
import {
  addModule,
  addQueue,
  AddQueueRequest,
  deleteModule,
  deleteQueue,
  DeleteQueueRequest,
  deleteResource,
  getInstance,
  getModule,
  getResource,
  Instance,
  killInstance,
  listInstances,
  listModuleDef,
  listModules,
  listQueues,
  listResources,
  Module,
  ModuleDef,
  ProjectResource,
  Queue,
  TypedQueryConfig,
  updateModule,
  updateQueue,
  UpdateQueueRequest,
} from "../redux-query";

// /project({projectId})/module
export const getCreateModuleRequest = (
  projectId: string,
  Module: Module,
  config?: TypedQueryConfig<string, Module>
) => {
  return mutateAsync(
    addModule({ projectId: projectId, module: Module }, config)
  );
};

// /project({projectId})/module
export const getModuleListRequest = (
  projectId: string,
  config?: TypedQueryConfig<{ modules: Array<Module> }, Array<Module>>
) => {
  return requestAsync(listModules({ projectId: projectId }, config));
};

// /module_def
export const getModuleDefinitionsListRequest = (
  config?: TypedQueryConfig<
    { modules_defs: Array<ModuleDef> },
    Array<ModuleDef>
  >
) => {
  return requestAsync(listModuleDef(config));
};

// /project({projectId})/module
export const getUpdateModuleRequest = (projectId: string, Module: Module) => {
  return mutateAsync(updateModule({ projectId: projectId, module: Module }));
};

// /project({projectId})/module({moduleId})
export const getDeleteModuleFromProjectRequest = (
  projectId: string,
  moduleId: string
) => {
  return mutateAsync(
    deleteModule({ projectId: projectId, moduleId: moduleId })
  );
};

// /project({projectId})/module({moduleId})
export const getSpecificModuleFromProjectRequest = (
  projectId: string,
  moduleId: string,
  config?: TypedQueryConfig<string, Module>
) => {
  return requestAsync(
    getModule({ projectId: projectId, moduleId: moduleId }, config)
  );
};

// /project({projectId})/queue
export const getProjectQueueList = (
  projectId: string,
  config?: TypedQueryConfig<string, Array<Queue>>
) => {
  return requestAsync(listQueues({ projectId: projectId }, config));
};

// /project({projectId})/queue
export const getCreateQueueRequest = (
  requestParams: AddQueueRequest,
  config?: TypedQueryConfig<string, Queue>
) => {
  return mutateAsync(addQueue(requestParams, config));
};

// /project({projectId})/queue
export const getUpdateProjectQueueRequest = (
  requestParams: UpdateQueueRequest,
  config?: TypedQueryConfig<string, Queue>
) => {
  return mutateAsync(updateQueue(requestParams, config));
};

// do zrobienia 1 nad tym req
// /project({projectId})/queue({moduleId})
export const getDeleteQueueFromProjectRequest = (
  requestParams: DeleteQueueRequest,
  config?: TypedQueryConfig<string, void>
) => {
  return mutateAsync(deleteQueue(requestParams, config));
};

// /project({projectId})/resource
export const getProjectResourceList = (
  projectId: string,
  config?: TypedQueryConfig<string, Array<ProjectResource>>
) => {
  return requestAsync(listResources({ projectId: projectId }, config));
};

// źle w api
/*
export const getCreateProjectResourceRequest = (
  projectId: string,
  resource: ProjectResource
  config?: TypedQueryConfig<string, ProjectResource>
) => {
  return mutateAsync(
    addResource({ projectId: projectId, resource: resource }, config)
  );
};
*/

// źle w api
/*
export const getUpdateProjectResourceRequest = (
  projectId: string,
  resource: ProjectResource,
  config?: TypedQueryConfig<string, ProjectResource>
) => {
  return mutateAsync(
    updateResource({ projectId: projectId, resource: resource  }, config)
  );
};
*/

// /project({projectId})/resource({resourceId})
export const getSpecificResourceFromProjectRequest = (
  projectId: string,
  resourceId: string,
  config?: TypedQueryConfig<string, ProjectResource>
) => {
  return requestAsync(
    getResource({ projectId: projectId, resourceId: resourceId }, config)
  );
};

// /project({projectId})/resource({resourceId})

export const getDeleteResourceFromProjectRequest = (
  projectId: string,
  resourceId: string,
  config?: TypedQueryConfig<string, void>
) => {
  return mutateAsync(
    deleteResource({ projectId: projectId, resourceId: resourceId }, config)
  );
};

// /project({projectId})/instance
export const getProjectInstanceListRequest = (
  projectId: string,
  config?: TypedQueryConfig<string, Array<Instance>>
) => {
  return requestAsync(listInstances({ projectId: projectId }, config));
};

// źle w api
// /project({projectId})/instance
/*
export const getCreateProjectInstanceRequest = (
  projectId: string,
  instance: Instance,
  config?: TypedQueryConfig<string, Instance>
) => {
  return mutateAsync(
    addInstance({ projectId: projectId, instance: instance }, config)
  );
};
*/
// źle w api
// /project({projectId})/instance
/*
export const getUpdateProjectInstanceRequest = (
  projectId: string,
  instance: Instance,
  config?: TypedQueryConfig<string, Instance>
) => {
  return mutateAsync(
    addInstance({ projectId: projectId, instance: instance }, config)
  );
*/

// /project({projectId})/instance({instanceId})

export const getSpecificProjectInstanceRequest = (
  projectId: string,
  instanceId: string,
  config?: TypedQueryConfig<string, Instance>
) => {
  return requestAsync(
    getInstance({ projectId: projectId, instanceId: instanceId }, config)
  );
};

// /project({projectId})/instance({instanceId})

export const getDeleteProjectInstanceRequest = (
  projectId: string,
  instanceId: string,
  config?: TypedQueryConfig<string, void>
) => {
  return mutateAsync(
    killInstance({ projectId: projectId, instanceId: instanceId }, config)
  );
};

// 2 ostatnie do przerobienia
