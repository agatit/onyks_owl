import { DiagramModel } from "@projectstorm/react-diagrams-core";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";
import createEngine, {
  DefaultDiagramState,
  DefaultLinkFactory,
} from "@projectstorm/react-diagrams";
import { OwlNodeFactory } from "../../Components/OwlNodes/OwlNodeFactory";
import { EditableLabelFactory } from "../../Components/CustomLinks/Labels/LabelFactory";
import { OwlQueueLinkFactory } from "../../Components/OwlQueueLinks/OwlQueueLinkFactory";
import { DeleteItemsAction } from "@projectstorm/react-canvas-core";
import { OwlQueueFactory } from "../../Components/OwlQueue/OwlQueueFactory";

export const engineActionTypes = {
  SET_DIAGRAM_MODEL: "SET_DIAGRAM_MODEL",
  REPAINT_CANVAS: "REPAINT_CANVAS",
  ZOOM_TO_FIT: "ZOOM_TO_FIT",
};

const initialState = {
  engine: getEngineWithConfig(),
  test: true,
  currentModel: undefined,
};

function getEngineWithConfig(): DiagramEngine {
  const engine = createEngine({
    registerDefaultDeleteItemsAction: false,
  });
  const state = engine.getStateMachine().getCurrentState();
  if (state instanceof DefaultDiagramState) {
    state.dragNewLink.config.allowLooseLinks = false;
  }
  engine.maxNumberPointsPerLink = 0;
  engine.getNodeFactories().registerFactory(new OwlNodeFactory());
  engine.getLinkFactories().registerFactory(new OwlQueueLinkFactory());
  engine.getNodeFactories().registerFactory(new OwlQueueFactory());
  //engine.getLinkFactories().registerFactory(new DefaultLinkFactory());
  engine
    .getActionEventBus()
    .registerAction(new DeleteItemsAction({ keyCodes: [46] }));

  return engine;
}

interface engineAction {
  type: string;
  diagramModel?: DiagramModel;
}

export const engineReducer = (state = initialState, action: engineAction) => {
  switch (action.type) {
    case engineActionTypes.SET_DIAGRAM_MODEL:
      if (action.diagramModel) state.engine.setModel(action.diagramModel);
      return { ...state, currentModel: action.diagramModel, test: !state.test };
    case engineActionTypes.REPAINT_CANVAS:
      state.engine.repaintCanvas();
      return state;
    case engineActionTypes.ZOOM_TO_FIT:
      state.engine.zoomToFit();
      return state;
    default:
      return state;
  }
};
