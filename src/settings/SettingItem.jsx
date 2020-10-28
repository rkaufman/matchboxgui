import React from 'react'

const SettingItem = (props) => {
    return (<div className="setting-item" onClick={props.click} data-id={props.dataItem.id}>
                <span className="vertical-center" style={{ width: "100%" }}>
                    <div style={{float: "left"}}>{props.dataItem.label} </div>
                    <span style={{ float: "right" }} className="fa fa-chevron-right fa-2x"/>
                </span>
            </div>);
}

export default SettingItem;
