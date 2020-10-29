import React from 'react'

const SettingItem = (props) => {
  let brd = { border: 'none' };
  if(props.dataItem.hasChanges === true){brd = {border: '1px solid red'}}
    return (<div className="setting-item" style={brd} onClick={props.click} data-id={props.dataItem.id}>
                <span className="vertical-center" style={{ width: "100%" }}>
                    <div style={{float: "left", paddingLeft: '1em'}}>{props.dataItem.label} </div>
                    <span style={{ float: "right", paddingRight: '1em' }} className="fa fa-chevron-right fa-2x"/>
                </span>
            </div>);
}

export default SettingItem;
