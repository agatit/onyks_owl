import * as React from "react";

import { EditableLabelModel } from "./LabelModel";
import styled from "@emotion/styled";

export interface FlowAliasLabelWidgetProps {
  model: EditableLabelModel;
}

namespace S {
  export const Label = styled.div`
    user-select: none;
    pointer-events: auto;
    width: 20px;
  `;
}

export const EditableLabelWidget: React.FunctionComponent<FlowAliasLabelWidgetProps> =
  (props) => {
    const [str, setStr] = React.useState(props.model.value);

    return (
      <S.Label>
        <input
          value={str}
          style={styledInput}
          onChange={(event) => {
            const newVal = event.target.value;
            setStr(newVal);
            props.model.value = newVal;
          }}
        />
      </S.Label>
    );
  };

const styledInput = {
  width: "100px",
};
