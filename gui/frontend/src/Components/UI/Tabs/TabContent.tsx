interface TabContentProps {
  currentTab: string;
  selectedTabValue: string;
  children?: React.ReactNode;
}

const TabContent = (props: TabContentProps) => {
  const tabSelected = props.currentTab === props.selectedTabValue;

  if (tabSelected) return <div>{props.children}</div>;

  return null;
};

export default TabContent;
