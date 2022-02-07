import { DefaultNodeModel } from "@projectstorm/react-diagrams";
import { deleteNode } from "../../store/Actions/nodeListActions";
import { deleteQueue, selectedQueue } from "../../store/Actions/queueActions";
import { getDeleteQueueFromProjectRequest } from "../../store/Queries/project_editor_queries";
import { getQueueParamsRequest } from "../../store/Queries/property_editor_queries";
import { QueueParamListConfig } from "../../store/QueryConfigs/property_query_configs";
import { Project } from "../../store/redux-query";
import store from "../../store/store";

export interface OwlQueueProps {
  id?: string;
  name?: string;
  project?: Project;
  ports?: any;
}

export class OwlQueueModel extends DefaultNodeModel {
  id: string;
  name: string;
  project: Project;

  constructor(options: OwlQueueProps = {}) {
    super({
      ...options,
      type: "OwlQueue",
      name: "Kolejka",
      color: "gray",
    });
    this.id = options.id || "Initial_Queue_ID";
    this.name = options.name || "Initial Queue Name";
    this.project = options.project || {
      id: "Test",
      name: "Initial_name",
    };
    this.addInPort("Wejście");
    this.addOutPort("Wyjście");
    this.registerListener({
      entityRemoved: () => {
        store.dispatch(
          getDeleteQueueFromProjectRequest({
            projectId: this.project.id,
            moduleId: "Do_zmiany",
          })
        );
        store.dispatch(deleteQueue(this));
        store.dispatch(deleteNode(this));
      },
      selectionChanged: () => {
        if (this.isSelected()) {
          store.dispatch(
            getQueueParamsRequest(
              { projectId: this.project.id, queueId: this.id },
              QueueParamListConfig
            )
          );
          store.dispatch(selectedQueue(this));
        }
      },
    });
  }

  serialize() {
    return {
      ...super.serialize(),
      position: super.getPosition(),
      name: this.name,
      project: this.project,
      id: this.id,
    };
  }
}
