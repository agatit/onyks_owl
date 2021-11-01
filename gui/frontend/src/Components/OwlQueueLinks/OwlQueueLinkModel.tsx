import {
  DefaultLabelModel,
  DefaultLinkModel,
} from "@projectstorm/react-diagrams";
import { deleteQueue, selectedQueue } from "../../store/Actions/queueActions";
import {
  getCreateQueueRequest,
  getDeleteQueueFromProjectRequest,
} from "../../store/Queries/project_editor_queries";
import { getQueueParamsRequest } from "../../store/Queries/property_editor_queries";
import { QueueParamListConfig } from "../../store/QueryConfigs/property_query_configs";
import { Project } from "../../store/redux-query";
import store from "../../store/store";
import { EditableLabelModel } from "../CustomLinks/Labels/LabelModel";

export interface OwlQueueLinkOptions {
  id?: string;
  name?: string;
  project?: Project;
}

export class OwlQueueLinkModel extends DefaultLinkModel {
  id: string;
  name: string;
  project: Project;

  constructor(options: OwlQueueLinkOptions = {}) {
    super({
      type: "OwlQueue",
    });
    this.id = options.id || "Initial_Link_ID";
    this.name = options.name || "Initial Link Name";
    this.project = options.project || {
      id: "Test",
      name: "Initial_name",
    };
    this.registerListener({
      targetPortChanged: () => {
        if (this.sourcePort) {
          store.dispatch(
            getCreateQueueRequest({ projectId: this.project.id, queue: this })
          );
          //this.addLabel(new EditableLabelModel({ value: "Test" }));
          // store.dispatch(selectedQueue(this));
        }
      },
      entityRemoved: () => {
        if (this.targetPort) {
          store.dispatch(
            getDeleteQueueFromProjectRequest({
              projectId: this.project.id,
              moduleId: "Do_zmiany",
            })
          );
          store.dispatch(deleteQueue(this));
        }
      },
      selectionChanged: () => {
        if (this.isSelected() && this.targetPort) {
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
}
