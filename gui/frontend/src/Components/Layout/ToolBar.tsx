import classses from "./Toolbar.module.css";
import { connect, useSelector } from "react-redux";
import { OwlNodeModel } from "../OwlNodes/OwlNodeModel";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCube,
  faFile,
  faShare,
  faShareAlt,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { isQueueSelected } from "../../store/selectors/queueSelectors";
import ModulePropEditor from "../UI/Menu-UI/Editors/ModulePropEditor";
import QueuePropEdtior from "../UI/Menu-UI/Editors/QueuePropEdtior";
import Tab from "../UI/Tabs/Tab";
import TabContainer from "../UI/Tabs/TabContainer";
import { useState } from "react";
import TabContent from "../UI/Tabs/TabContent";
import ProjectEditor from "../UI/Menu-UI/Editors/ProjectEditor";

// REFERENCJE CHYBA DO WYWALENIA!!!!!!!!!!!!!

interface toolBarProps {
  node: OwlNodeModel;
  projectId: string;
}

function ToolBar(props: toolBarProps) {
  const [activeTab, setActiveTab] = useState("1");

  const handleTabChange = (tabValue: string) => {
    setActiveTab(tabValue);
  };

  const queueSelected: boolean = useSelector(isQueueSelected);

  return (
    <div className={classses.toolBar}>
      <TabContainer
        tabs={MenuTabs}
        onChange={handleTabChange}
        currentTab={activeTab}
      />
      <div className={classses.tabContent}>
        <TabContent currentTab={activeTab} selectedTabValue="1">
          <ModulePropEditor projectId={props.projectId} />
        </TabContent>
        <TabContent currentTab={activeTab} selectedTabValue="2">
          <QueuePropEdtior projectId={props.projectId} />
        </TabContent>
        <TabContent currentTab={activeTab} selectedTabValue="3">
          <ProjectEditor projectId={props.projectId} />
        </TabContent>
      </div>
    </div>
  );

  /*
  {
    if (queueSelected) {
      return <QueuePropEdtior projectId={props.projectId} />;
    }
  }

  return (
    <div className={classses.toolBar}>
      
    </div>
  );
  */
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    test: state.nodesData.test,
  };
};

const connector = connect(mapStateToProps)(ToolBar);

export default connector;

const MenuTabs: JSX.Element[] = [
  <Tab
    onClick={() => {}}
    active={true}
    label="Moduł"
    value={"1"}
    icon={faCube}
  />,
  <Tab
    onClick={() => {}}
    active={false}
    label="Kolejka"
    value={"2"}
    icon={faShareAlt}
  />,
  <Tab
    onClick={() => {}}
    active={false}
    label="Projekt"
    value={"3"}
    icon={faFile}
  />,
];

//const nameInputRef = useRef<HTMLInputElement>(null);
//const refArray = useRef<any>([]);

//refArray.current = [];

/*
  const addToRefs = (el: HTMLInputElement) => {
    if (el && !refArray.current.includes(el)) {
      refArray.current.push(el);
    }
  };

  
*/
