import Module from "module";
import { useEffect } from "react";
import { ListGroup } from "react-bootstrap";
import { connect } from "react-redux";
import { getModuleListRequest } from "../../../store/Queries/project_editor_queries";
import { ModuleListRequestConfig } from "../../../store/QueryConfigs/module_query_configs";
import {
  clearModuleList,
  selectModuleList,
} from "../../../store/selectors/moduleSelectors";
import store from "../../../store/store";
import ListModule from "../ListModule";

import classes from "./ModuleList.module.css";

interface ModuleListProps {
  projectId: string;
  modules: Module[];
  getModuleList: (projectId: string) => void;
  clearModuleList: () => void;
}

function ModuleList(props: ModuleListProps) {
  useEffect(() => {
    props.clearModuleList();
    setTimeout(() => {
      props.getModuleList(props.projectId);
      console.log(store.getState().entities);
    }, 3000);
  }, []);

  const wrapListElement = (module: Module, index: number) => {
    return (
      <ListGroup.Item as="li" key={index} bsPrefix={classes.test}>
        <ListModule module={module} />
      </ListGroup.Item>
    );
  };

  return (
    <ListGroup as="ul">
      {props.modules &&
        props.modules.map((module, index) => wrapListElement(module, index))}
    </ListGroup>
  );
}

const mapStateToProps = (state: any) => {
  return {
    modules: selectModuleList(state),
  };
};

const mapDispatchToProps = (dispatch: any, state: any) => {
  return {
    getModuleList: (projectId: string) => {
      dispatch(getModuleListRequest(projectId, ModuleListRequestConfig));
    },
    clearModuleList: () => {
      clearModuleList(state);
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ModuleList);
