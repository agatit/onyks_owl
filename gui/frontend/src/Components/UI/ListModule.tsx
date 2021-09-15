import calsses from "./ListModule.module.css";

function ListModule(props: any) {
  return (
    <div
      className={calsses.module}
      draggable="true"
      onDragStart={(event) => {
        event.dataTransfer.setData(
          "diagram-node",
          JSON.stringify(props.module)
        );
      }}
    >
      {props.module.name}
    </div>
  );
}

export default ListModule;
