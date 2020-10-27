import React from 'react'
import { Checkbox } from '@progress/kendo-react-inputs';

const InputSelector = (props) => {
    if (props._controlType == undefined) return <span/>;
    let input = null;
    switch (props._controlType._name) {
        case 'tb':
            input = <input type="text" placeholder={props._placeholder} data-id={props._settingId} value={props._setting} onChange={props.settingChanged}/>;
            break;
        case 'checkbox':
            input =
                <div className="mx-checkbox"><input type="checkbox" checked={props._setting.toLowerCase() == 'true'} id={
props._settingId.toString()} data-id={props._settingId} onChange={props.settingChanged}/><label htmlFor={
props._settingId.toString()}></label></div>;
            break;
        default:
            input = <span></span>;
    }
    return (<div>
                  <label>{props._label}</label>
                  {input}
                  <p>{props._help}</p>
                  </div>);
            
}

export default InputSelector;