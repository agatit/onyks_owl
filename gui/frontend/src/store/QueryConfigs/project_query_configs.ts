import { QueryConfig } from "redux-query";
import { Project } from "../redux-query";

export const ProjectListRequestConfig: QueryConfig = {
  url: "",
  transform: (response: Project) => {
    console.log(response);
    return {
      projects: response,
    };
  },
  update: {
    projects: (prevVal, newVal) => newVal,
  },
};
