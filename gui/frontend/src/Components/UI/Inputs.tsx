import React, { useState, forwardRef } from "react";

enum InputType {
  button = "button",
  checkbox = "checkbox",
  color = "color",
  date = "date",
  datetimelocal = "datetime-local",
  email = "email",
  file = "file",
  hidden = "hidden",
  image = "image",
  month = "month",
  number = "number",
  password = "password",
  radio = "radio",
  range = "range",
  reset = "reset",
  search = "search",
  submit = "submit",
  tel = "tel",
  text = "text",
  time = "time",
  url = "url",
  week = "week",
}

interface BaseInputProps {
  id: string;
  ref?: React.RefObject<HTMLInputElement>;
  initValue: string;
  labelText: string;
  type?: InputType;
  label?: string;
  onChangeAction: (
    event: React.ChangeEvent<HTMLInputElement>,
    propertyName: string,
    refNum: number
  ) => void;
}

interface NumberInputProps extends BaseInputProps {
  min?: string;
  max?: string;
  step?: string;
  propName: string;
}

function NumberInputBase(props: NumberInputProps, ref: any) {
  //const [currentValue, setCurrentValue] = useState(props.initValue);

  return (
    <div>
      {props.label == null ? (
        <label htmlFor={props.id}>{props.labelText}</label>
      ) : null}
      <input
        id={props.id}
        type="number"
        onChange={(e) => {
          props.onChangeAction(e, props.propName, 0);
        }}
        value={props.initValue}
        min={props.min}
        max={props.max}
        step={props.step}
      />
    </div>
  );
}

export const NumberInput = forwardRef(NumberInputBase);

interface TextInputProps extends BaseInputProps {
  minLen?: number;
  maxLen?: number;
  step?: string;
  propName: string;
  refNum: number;
}

function TextInputBase(props: TextInputProps, ref: any) {
  const [currentValue, setCurrentValue] = useState(props.initValue);

  function handleChange() {}

  return (
    <div>
      {props.label == null ? (
        <label htmlFor={props.id}>{props.labelText}</label>
      ) : null}
      <input
        id={props.id}
        type="text"
        onChange={(e) => {
          props.onChangeAction(e, props.propName, props.refNum);
        }}
        ref={ref}
        value={props.initValue}
        minLength={props.minLen}
        maxLength={props.maxLen}
      />
    </div>
  );
}

export const TextInput = forwardRef(TextInputBase);
