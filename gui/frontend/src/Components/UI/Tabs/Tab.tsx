import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styled from "@emotion/styled";
import { IconProp } from "@fortawesome/fontawesome-svg-core";

interface TabProps {
  onClick: (e: any) => void;
  icon?: IconProp;
  active: boolean;
  label?: string;
  value: string;
}

const Tab = (props: TabProps) => {
  return (
    <StyledTab
      color="white"
      background="black"
      onClick={() => {
        props.onClick(props.value);
      }}
      active={props.active}
    >
      {props.icon && <FontAwesomeIcon icon={props.icon} />}
      {props.label}
    </StyledTab>
  );
};

//css
const StyledTab = styled.button<{
  color: string;
  background: string;
  active: boolean;
}>`
  width: 100%;
  background-color: ${(p) => p.background};
  color: ${(p) => p.color};
  border: none;
  padding: 10px 0px;
  font-size: 1.25rem;
  ${(p) =>
    p.active &&
    `
      color: #feca57;
      font-weight: bold;
    `}
  ${(p) => !p.active && "opacity: 65%"}
`;

export default Tab;
