import styled from "@emotion/styled";
import { cloneElement } from "react";
import Tab from "./Tab";

interface TabContainerProps {
  tabs: any[];
  onChange: (tabValue: string) => void;
  currentTab: string;
}

const TabContainer = (props: TabContainerProps) => {
  const tabs = props.tabs.map((tab) => {
    const handleClick = (e: any) => {
      props.onChange(tab.props.value);
    };

    return cloneElement(tab, {
      key: tab.props.value,
      active: tab.props.value === props.currentTab,
      onClick: handleClick,
    });
  });

  return (
    <StyledTabContainer>
      <TabHolder>{tabs}</TabHolder>
    </StyledTabContainer>
  );
};

export default TabContainer;

const StyledTabContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

const TabHolder = styled.div`
  display: flex;
`;
