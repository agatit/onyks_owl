import { DefaultLinkModel } from "@projectstorm/react-diagrams";
import { Project } from "../../store/redux-query";

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
      type: "OwlQueueLink",
    });
    this.setColor("white");
    this.id = options.id || "Initial_Link_ID";
    this.name = options.name || "Initial Link Name";
    this.project = options.project || {
      id: "Test",
      name: "Initial_name",
    };
    // this.registerListener({
    //   targetPortChanged: () => {
    //     if (this.sourcePort) {
    //       store.dispatch(
    //         getCreateQueueRequest({ projectId: this.project.id, queue: this })
    //       );
    //       //this.addLabel(new EditableLabelModel({ value: "Test" }));
    //       // store.dispatch(selectedQueue(this));
    //     }
    //   },
    //   // entityRemoved: () => {
    //   //   if (this.targetPort) {
    //   //     store.dispatch(
    //   //       getDeleteQueueFromProjectRequest({
    //   //         projectId: this.project.id,
    //   //         moduleId: "Do_zmiany",
    //   //       })
    //   //     );
    //   //     store.dispatch(deleteQueue(this));
    //   //   }
    //   // },
    //   // selectionChanged: () => {
    //   //   if (this.isSelected() && this.targetPort) {
    //   //     store.dispatch(
    //   //       getQueueParamsRequest(
    //   //         { projectId: this.project.id, queueId: this.id },
    //   //         QueueParamListConfig
    //   //       )
    //   //     );
    //   //     store.dispatch(selectedQueue(this));
    //   //   }
    //   // },
    // });
  }
}
