import { useEffect } from "react";
import { ListGroup } from "react-bootstrap";
import { connect } from "react-redux";
import { getModuleDefinitionsListRequest } from "../../../store/Queries/project_editor_queries";
import { ModuleListDefsRequestConfig } from "../../../store/QueryConfigs/module_query_configs";
import { ModuleDef } from "../../../store/redux-query";
import {
  clearModuleList,
  selectModuleDefsList,
} from "../../../store/selectors/moduleSelectors";
import ListModule from "../ListModule";

import classes from "./ModuleList.module.css";

interface ModuleListProps {
  projectId: string;
  modules: ModuleDef[];
  getModuleDefList: () => void;
  clearModuleList: () => void;
}

function ModuleList(props: ModuleListProps) {
  useEffect(() => {
    props.clearModuleList();
    setTimeout(() => {
      props.getModuleDefList();
    }, 3000);
  }, []);

  const wrapListElement = (module: ModuleDef, index: number) => {
    return (
      <ListGroup.Item as="li" key={index} bsPrefix={classes.test}>
        <ListModule module={module} />
      </ListGroup.Item>
    );
  };

  if (!props.modules) {
    return <div>Ładowanie modułów</div>;
  }

  return (
    <ListGroup as="ul">
      {props.modules &&
        props.modules.map((module, index) => wrapListElement(module, index))}
    </ListGroup>
  );
}

const mapStateToProps = (state: any) => {
  return {
    modules: selectModuleDefsList(state),
  };
};

const mapDispatchToProps = (dispatch: any, state: any) => {
  return {
    getModuleDefList: () => {
      dispatch(getModuleDefinitionsListRequest(ModuleListDefsRequestConfig));
    },
    clearModuleList: () => {
      clearModuleList(state);
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ModuleList);
