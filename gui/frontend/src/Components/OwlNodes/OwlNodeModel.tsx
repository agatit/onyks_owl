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
  color: string;
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

  constructor(options: NodeModelOptions = {}) {
    super({
      ...options,
      type: "Owl-node",
    });
    this.color = options.color || "White";
    this.title = options.title || "Node";
    this.content = options.content || undefined;
    this.source = options.source || false;
    this.params = {};
    this.parameters = options.parameters || []; // do usunięcia
    this.module_id = options.module_id || "node";
    this.id = options.id || "testId";
    this.moduleDefId = options.moduleDefId || "test ModuleDefId";
    this.project = options.project || {
      id: "initial ID",
      name: "Initial name",
    };
    this.input = options.input || { id: "initial ID", name: "Initial name" };
    this.output = options.output || { id: "initial ID", name: "Initial name" };
    this.name = options.name || "Initial module name";
    this.inputPortModel = new OwlDefaultPort({
      in: true,
      name: "In",
    });
    this.outputPortModel = new OwlDefaultPort({
      in: false,
      name: "Out",
    });

    if (this.content && !this.source) {
      this.addPort(this.inputPortModel);
    }
    this.addPort(this.outputPortModel);
  }

  serialize() {
    return {
      ...super.serialize(),
      color: this.color,
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
    this.color = event.data.color;
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
