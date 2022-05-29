import { ListGroup, Spinner } from "react-bootstrap";
import { connect } from "react-redux";
import { toast } from "react-toastify";
import { useRequest } from "redux-query-react";
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
  clearModuleList: () => void;
}

function ModuleList(props: ModuleListProps) {
  const [{ isPending, status }, refresh] = useRequest(
    ModuleListDefsRequestConfig
  );

  const wrapListElement = (module: ModuleDef, index: number) => {
    return (
      <ListGroup.Item as="li" key={index} bsPrefix={classes.moduleList}>
        <ListModule module={module} />
      </ListGroup.Item>
    );
  };

  if (isPending) {
    return (
      <>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <h4>Trwa ładowanie modułów!</h4>
      </>
    );
  }

  if (typeof status === "number" && (status >= 400 || status < 200)) {
    toast.error("Brak połączenia z serwerem!");
    return <h6>Brak połączenia, spróbuj odświeżyć stronę!</h6>;
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
    clearModuleList: () => {
      clearModuleList(state);
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(ModuleList);
