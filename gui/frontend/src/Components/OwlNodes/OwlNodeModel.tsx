import {
  NodeModel as StormNodeModel,
  DefaultPortModel,
} from "@projectstorm/react-diagrams";
import {
  BaseModelOptions,
  DeserializeEvent,
} from "@projectstorm/react-canvas-core";
import { ModuleParam, Project, Queue } from "../../store/redux-query";
import { OwlDefaultPort } from "../OwlPorts/OwlDefaultPort";

export interface NodeModelOptions extends BaseModelOptions {
  color?: string;
  title?: string;
  content?: string;
  source?: boolean;
  description?: string;
  module_id?: string;
  id?: string;
  moduleDefId?: string;
  project?: Project;
  input?: Queue;
  output?: Queue;
  name?: string;
  parameters?: Array<ModuleParam>;
}

export class OwlNodeModel extends StormNodeModel {
  headerColor: string;
  bodyColor: string;
  title: string;
  content: string | undefined;
  source: boolean;
  module_id: string;
  id: string;
  params: { [key: string]: any };
  moduleDefId: string;
  project: Project;
  input: Queue;
  output: Queue;
  name?: string;
  inputPortModel: DefaultPortModel;
  outputPortModel: DefaultPortModel;
  parameters: Array<ModuleParam>;
  description: string;

  constructor(options: NodeModelOptions = {}) {
    super({
      ...options,
      type: "Owl-node",
    });

    this.headerColor = options?.color || "White";
    this.bodyColor = "#141414";
    this.title = options?.title || "Node";
    this.description = options?.description || "Brak opisu modułu";
    this.content = options?.content || "Testowy content";
    this.source = options?.source || false;
    this.params = {};
    this.parameters = options?.parameters || [];
    this.module_id = options?.module_id || "node";
    this.id = options?.id || "testId";
    this.moduleDefId = options?.moduleDefId || "test ModuleDefId";
    this.project = options?.project || {
      id: "initial ID",
      name: "Initial name",
    };
    this.input = options?.input || { id: "initial ID", name: "Initial name" };
    this.output = options?.output || { id: "initial ID", name: "Initial name" };
    this.name = options?.name || "Initial module name";
    this.inputPortModel = new OwlDefaultPort({
      in: true,
      name: "In",
    });
    this.outputPortModel = new OwlDefaultPort({
      in: false,
      name: "Out",
    });

    if (!this.source) {
      this.addPort(this.inputPortModel);
    }
    this.addPort(this.outputPortModel);
  }

  serialize() {
    return {
      ...super.serialize(),
      // color: this.color,
      title: this.title,
      content: this.content,
      source: this.source,
      input: this.input,
      output: this.output,
      name: this.name,
      project: this.project,
      moduleDefId: this.moduleDefId,
      id: this.id,
      module_id: this.module_id,
    };
  }

  deserialize(event: DeserializeEvent<this>): void {
    super.deserialize(event);
    //this.headerColor = event.data.color;
    //this.bodyColor = event.data
    this.title = event.data.title;
    this.content = event.data.content;
    this.source = event.data.source;
    this.input = event.data.input;
    this.output = event.data.output;
    this.id = event.data.id;
    this.module_id = event.data.module_id;
    this.project = event.data.project;
    this.moduleDefId = event.data.moduleDefId;
  }
}
