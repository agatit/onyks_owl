import { ModuleDef } from "../../store/redux-query";
import calsses from "./ListModule.module.css";

export const moduleTransferName = "diagram-node";

interface ListModuleProps {
  module: ModuleDef;
}

function ListModule(props: ListModuleProps) {
  return (
    <div
      className={calsses.module}
      draggable="true"
      onDragStart={(event) => {
        event.dataTransfer.setData(
          moduleTransferName,
          JSON.stringify(props.module)
        );
      }}
    >
      {props.module.name}
    </div>
  );
}

export default ListModule;
