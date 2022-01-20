import classes from "./TabSection.module.css";

interface TabSectionProps {
  title: string;
  children: any;
}

function TabSection(props: TabSectionProps) {
  return (
    <div className={classes.sectionWindow}>
      <div className={classes.sectionTitle}>{props.title}</div>
      {props.children}
    </div>
  );
}

export default TabSection;
