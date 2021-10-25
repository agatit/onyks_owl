import { mutateAsync, QueryConfig, requestAsync } from "redux-query";
import {
  addProject,
  deleteProject,
  listProjects,
  Project,
  updateProject,
} from "../redux-query";

export const getCreateProjectRequest = (project: Project) => {
  return mutateAsync(addProject({ project: project }));
};

export const getProjectListRequest = (config?: QueryConfig) => {
  return requestAsync(listProjects(config));
};

export const getUpdateProjectRequest = (project: Project) => {
  return mutateAsync(updateProject({ project: project }));
};

export const getDeleteProjectRequest = (projectId: string) => {
  return mutateAsync(deleteProject({ projectId: projectId }));
};
