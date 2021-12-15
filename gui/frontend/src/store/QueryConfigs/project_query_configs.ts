import { QueryConfig } from "redux-query";
import { Configuration, Project, TypedQueryConfig } from "../redux-query";

export const ProjectListRequestConfig: QueryConfig = {
  url: `${Configuration.basePath}/project`,
  transform: (response: Project) => {
    console.log("W zapytaniu:" + response);
    return {
      projects: response,
    };
  },
  update: {
    projects: (prevVal, newVal) => newVal,
  },
};

export const ProjectRequestConfig: TypedQueryConfig<
  { project: Project },
  Project
> = {
  transform: (response: Project) => {
    return {
      project: response,
    };
  },
  update: {
    project: (prevVal, newVal) => newVal,
  },
  force: true,
};
