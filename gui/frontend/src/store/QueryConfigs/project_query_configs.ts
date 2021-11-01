import { QueryConfig } from "redux-query";
import { Project, TypedQueryConfig } from "../redux-query";

export const ProjectListRequestConfig: QueryConfig = {
  url: "",
  transform: (response: Project) => {
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
    console.log("W zapytaniu:" + response);
    return {
      project: response,
    };
  },
  update: {
    project: (prevVal, newVal) => newVal,
  },
  force: true,
};
