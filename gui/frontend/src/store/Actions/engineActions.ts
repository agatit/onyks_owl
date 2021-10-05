import { engineActionTypes } from "../Reducers/engineReducer";
import { DiagramModel } from "@projectstorm/react-diagrams-core";

export const setModel = (model: DiagramModel) => ({
  type: engineActionTypes.SET_DIAGRAM_MODEL,
  model,
});

export const repaintCanvas = () => ({
  type: engineActionTypes.REPAINT_CANVAS,
});
