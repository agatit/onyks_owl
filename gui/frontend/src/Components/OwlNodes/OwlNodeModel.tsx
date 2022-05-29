import {
  NodeModel as StormNodeModel,
  DefaultPortModel,
} from "@projectstorm/react-diagrams";
import {
  BaseModelOptions,
  DeserializeEvent,
} from "@projectstorm/react-canvas-core";
import { Module, ModuleParam, Project, Queue } from "../../store/redux-query";
import { OwlDefaultPort } from "../OwlPorts/OwlDefaultPort";

export interface NodeModelOptions extends BaseModelOptions {
  color?: string;
  title?: string;
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
  params?: Array<ModuleParam>;
}

export class OwlNodeModel extends StormNodeModel implements Module {
  headerColor: string;
  bodyColor: string;
  source: boolean;
  id: string;
  moduleDefId: string;
  project: Project;
  input: Queue;
  output: Queue;
  name?: string;
  inputPortModel: DefaultPortModel;
  outputPortModel: DefaultPortModel;
  parameters: Array<any>;
  description: string;

  constructor(options: NodeModelOptions = {}) {
    super({
      ...options,
      type: "Owl-node",
    });
    this.name = options?.name || "Initial module name";
    this.headerColor = options?.color || "#FFFFFF";
    this.bodyColor = "#141414";
    this.description = options?.description || "Brak opisu modułu";
    this.source = options?.source || false;
    this.parameters = objectToArrayHelper(options?.params) || []; // metoda na potrzeby obecnej implementacji (do usunięcia w przyszłości)
    this.id = options?.id || "testId";
    this.moduleDefId = options?.moduleDefId || "test ModuleDefId";
    this.project = options?.project || {
      id: "initial ID",
      name: "Initial name",
    };
    this.input = options?.input || { id: "initial ID", name: "Initial name" };
    this.output = options?.output || { id: "initial ID", name: "Initial name" };
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
      source: this.source,
      input: this.input,
      output: this.output,
      name: this.name,
      project: this.project,
      moduleDefId: this.moduleDefId,
      id: this.id,
    };
  }

  deserialize(event: DeserializeEvent<this>): void {
    super.deserialize(event);
    this.source = event.data.source;
    this.input = event.data.input;
    this.output = event.data.output;
    this.id = event.data.id;
    this.project = event.data.project;
    this.moduleDefId = event.data.moduleDefId;
  }
}

//Metoda na potrzeby obecnej implementacji zapytań - do usunięcia po uzupełnieniu.
const objectToArrayHelper = (obj: any) => {
  return Object.entries(obj).map(([k, v]) => ({ [k]: v }));
};
