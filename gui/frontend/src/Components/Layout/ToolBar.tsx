import classses from "./Toolbar.module.css";
import { connect } from "react-redux";
import { OwlNodeModel } from "../OwlNodes/OwlNodeModel";
import { faCube, faFile, faShareAlt } from "@fortawesome/free-solid-svg-icons";
import ModulePropEditor from "../UI/Menu-UI/Editors/ModulePropEditor";
import QueuePropEdtior from "../UI/Menu-UI/Editors/QueuePropEdtior";
import Tab from "../UI/Tabs/Tab";
import TabContainer from "../UI/Tabs/TabContainer";
import { useState } from "react";
import TabContent from "../UI/Tabs/TabContent";
import ProjectEditor from "../UI/Menu-UI/Editors/ProjectEditor";
import AddQueueForm from "../UI/Menu-UI/AddQueueForm";
import DiagramObjectMenageList from "../UI/Menu-UI/DiagramObjectMenageList";
import { DiagramEngine } from "@projectstorm/react-diagrams";

interface toolBarProps {
  node: OwlNodeModel;
  projectId: string;
  engine: DiagramEngine;
}

function ToolBar(props: toolBarProps) {
  const [activeTab, setActiveTab] = useState("1");

  const moduleEditorTabSelectValue = "1";
  const queueEditorTabSelectValue = "2";
  const projectEditorTabSelectValue = "3";

  const handleTabChange = (tabValue: string) => {
    setActiveTab(tabValue);
  };

  return (
    <div className={classses.toolBar}>
      <TabContainer
        tabs={MenuTabs}
        onChange={handleTabChange}
        currentTab={activeTab}
      />
      <div className={classses.tabContent}>
        <TabContent
          currentTab={activeTab}
          selectedTabValue={moduleEditorTabSelectValue}
        >
          <ModulePropEditor projectId={props.projectId} />
        </TabContent>
        <TabContent
          currentTab={activeTab}
          selectedTabValue={queueEditorTabSelectValue}
        >
          <AddQueueForm />
          <QueuePropEdtior projectId={props.projectId} />
        </TabContent>
        <TabContent
          currentTab={activeTab}
          selectedTabValue={projectEditorTabSelectValue}
        >
          <DiagramObjectMenageList />
          <ProjectEditor projectId={props.projectId} />
        </TabContent>
      </div>
    </div>
  );
}

const mapStateToProps = (state: any) => {
  return {
    node: state.nodesData.selectedNode,
    test: state.nodesData.test,
    engine: state.engineReducer.engine,
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
